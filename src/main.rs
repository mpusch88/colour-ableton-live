mod skin;

use eframe::egui;
use axum::{routing::get, Router};
use std::net::SocketAddr;
use tokio::runtime::Runtime;
use tokio::sync::oneshot;

#[derive(PartialEq)]
enum ViewMode {
    SideBySide,
    PreviewBelow,
    PreviewOff,
}

struct MyApp {
    web_server_enabled: bool,
    server_tx: Option<oneshot::Sender<()>>,
    rt: Runtime,
    active_skin: Option<skin::Skin>,
    show_settings: bool,
    view_mode: ViewMode,
    split_x: f32,
    split_y: f32,
}

impl Default for MyApp {
    fn default() -> Self {
        let default_skin = std::fs::read_to_string("Skins/Mid Dark - Blue.ask")
            .map_err(|e| eprintln!("Failed to read skin file: {}", e))
            .ok()
            .and_then(|xml| {
                skin::Skin::parse(&xml)
                    .map_err(|e| eprintln!("Failed to parse XML: {:?}", e))
                    .ok()
            });

        Self {
            web_server_enabled: false,
            server_tx: None,
            rt: Runtime::new().expect("Unable to create Tokio runtime"),
            active_skin: default_skin,
            show_settings: false,
            view_mode: ViewMode::PreviewBelow,
            split_x: 350.0,
            split_y: 250.0,
        }
    }
}

impl eframe::App for MyApp {
    fn ui(&mut self, ui: &mut egui::Ui, _frame: &mut eframe::Frame) {
        ui.horizontal(|ui| {
            ui.heading("Ableton Live 12 Skin Customizer");
            ui.with_layout(egui::Layout::right_to_left(egui::Align::Center), |ui| {
                if ui.button("⚙").clicked() {
                    self.show_settings = !self.show_settings;
                }
                if ui.button("📂 Import").clicked() {
                    if let Some(path) = rfd::FileDialog::new()
                        .add_filter("Ableton Skin", &["ask"])
                        .pick_file() 
                    {
                        if let Ok(xml) = std::fs::read_to_string(&path) {
                            if let Ok(parsed_skin) = skin::Skin::parse(&xml) {
                                self.active_skin = Some(parsed_skin);
                            }
                        }
                    }
                }
                if ui.button("🔄").on_hover_text("Reload Skins/Mid Dark - Blue.ask").clicked() {
                    match std::fs::read_to_string("Skins/Mid Dark - Blue.ask") {
                        Ok(xml) => match skin::Skin::parse(&xml) {
                            Ok(parsed_skin) => self.active_skin = Some(parsed_skin),
                            Err(e) => eprintln!("Parse error on reload: {:?}", e),
                        },
                        Err(e) => eprintln!("Read error on reload: {}", e),
                    }
                }
            });
        });
        ui.add_space(10.0);

        if self.show_settings {
            egui::Window::new("Settings").open(&mut self.show_settings).show(ui.ctx(), |ui| {
                ui.heading("App Layout");
                ui.horizontal(|ui| {
                    ui.radio_value(&mut self.view_mode, ViewMode::PreviewOff, "Preview Off");
                    ui.radio_value(&mut self.view_mode, ViewMode::PreviewBelow, "Vertical Split");
                    ui.radio_value(&mut self.view_mode, ViewMode::SideBySide, "Horizontal Split");
                });
                
                ui.separator();
                ui.heading("Web Server");
                ui.label("Web Server Settings (for premium UI / remote access)");
                ui.horizontal(|ui| {
                    if ui.checkbox(&mut self.web_server_enabled, "Enable Web Server").changed() {
                        if self.web_server_enabled {
                            // Start server
                            let (tx, rx) = oneshot::channel();
                            self.server_tx = Some(tx);

                            let app = Router::new().route("/", get(|| async { 
                                "Hello from Ableton Skin Customizer API!\nThe web frontend will live here." 
                            }));

                            let addr = SocketAddr::from(([127, 0, 0, 1], 3000));
                            
                            self.rt.spawn(async move {
                                if let Ok(listener) = tokio::net::TcpListener::bind(addr).await {
                                    println!("Web server started at http://{}", addr);
                                    let _ = axum::serve(listener, app)
                                        .with_graceful_shutdown(async {
                                            rx.await.ok();
                                        })
                                        .await;
                                    println!("Web server stopped.");
                                }
                            });
                        } else {
                            // Stop server
                            if let Some(tx) = self.server_tx.take() {
                                let _ = tx.send(());
                            }
                        }
                    }

                    if self.web_server_enabled {
                        ui.label("🟢 Running at http://127.0.0.1:3000");
                        if ui.button("Open in Browser").clicked() {
                            let _ = std::process::Command::new("cmd")
                                .args(&["/C", "start http://127.0.0.1:3000"])
                                .spawn();
                        }
                    } else {
                        ui.label("🔴 Stopped");
                    }
                });
            });
        }

        let min_size = match self.view_mode {
            ViewMode::SideBySide => egui::vec2(1000.0, 700.0),
            ViewMode::PreviewBelow => egui::vec2(600.0, 900.0),
            ViewMode::PreviewOff => egui::vec2(400.0, 400.0),
        };
        ui.ctx().send_viewport_cmd(egui::ViewportCommand::MinInnerSize(min_size));

        ui.add_space(10.0);
        match self.view_mode {
            ViewMode::SideBySide => {
                let avail_h = ui.available_height();
                ui.horizontal(|ui| {
                    ui.allocate_ui_with_layout(egui::vec2(self.split_x, avail_h), egui::Layout::top_down(egui::Align::Min), |ui| {
                        self.draw_color_settings(ui);
                    });
                    
                    let (id, rect) = ui.allocate_space(egui::vec2(4.0, avail_h));
                    let response = ui.interact(rect, id, egui::Sense::drag());
                    if response.dragged() {
                        self.split_x += response.drag_delta().x;
                        self.split_x = self.split_x.clamp(150.0, 2000.0);
                    }
                    if response.hovered() || response.dragged() {
                        ui.ctx().set_cursor_icon(egui::CursorIcon::ResizeHorizontal);
                    }
                    ui.painter().rect_filled(rect, 0.0, ui.visuals().widgets.noninteractive.bg_stroke.color);

                    let avail_w = ui.available_width();
                    ui.allocate_ui_with_layout(egui::vec2(avail_w, avail_h), egui::Layout::top_down(egui::Align::Min), |ui| {
                        self.draw_preview(ui);
                    });
                });
            }
            ViewMode::PreviewBelow => {
                let avail_w = ui.available_width();
                ui.vertical(|ui| {
                    ui.allocate_ui_with_layout(egui::vec2(avail_w, self.split_y), egui::Layout::top_down(egui::Align::Min), |ui| {
                        self.draw_color_settings(ui);
                    });
                    
                    let (id, rect) = ui.allocate_space(egui::vec2(avail_w, 4.0));
                    let response = ui.interact(rect, id, egui::Sense::drag());
                    if response.dragged() {
                        self.split_y += response.drag_delta().y;
                        self.split_y = self.split_y.clamp(150.0, 2000.0);
                    }
                    if response.hovered() || response.dragged() {
                        ui.ctx().set_cursor_icon(egui::CursorIcon::ResizeVertical);
                    }
                    ui.painter().rect_filled(rect, 0.0, ui.visuals().widgets.noninteractive.bg_stroke.color);

                    let avail_h = ui.available_height();
                    ui.allocate_ui_with_layout(egui::vec2(avail_w, avail_h), egui::Layout::top_down(egui::Align::Min), |ui| {
                        self.draw_preview(ui);
                    });
                });
            }
            ViewMode::PreviewOff => {
                self.draw_color_settings(ui);
            }
        }
    }
}

fn categorize_color(name: &str) -> &'static str {
    let lower = name.to_lowercase();
    if lower.contains("surface") { "Surface & Backgrounds" }
    else if lower.contains("browser") { "Browser" }
    else if lower.contains("control") || lower.contains("scroll") { "Controls & Scrollbars" }
    else if lower.contains("view") || lower.contains("chooser") { "Views & Choosers" }
    else if lower.contains("text") { "Text" }
    else if lower.contains("meter") { "Meters" }
    else if lower.contains("automation") || lower.contains("grid") || lower.contains("arrange") || lower.contains("track") || lower.contains("timeline") { "Arrangement & Tracks" }
    else if lower.contains("clip") { "Clips" }
    else if lower.contains("retro") || lower.contains("threshold") || lower.contains("display") || lower.contains("bipolar") || lower.contains("device") || lower.contains("lcd") || lower.contains("eq") || lower.contains("spectrum") { "Devices & Graphs" }
    else { "Misc" }
}

impl MyApp {
    fn draw_color_settings(&mut self, ui: &mut egui::Ui) {
        ui.push_id("settings_scroll", |ui| {
            egui::ScrollArea::both().auto_shrink([false; 2]).show(ui, |ui| {
                ui.heading("Color Settings");
                ui.separator();

                if let Some(active_skin) = &mut self.active_skin {
                    ui.add_space(10.0);
                    ui.label(format!("Loaded {} colors", active_skin.colors.len()));
                    
                    let mut any_changed = false;
                    let categories = [
                        "Surface & Backgrounds", "Browser", "Controls & Scrollbars", 
                        "Views & Choosers", "Text", "Meters", "Arrangement & Tracks", 
                        "Clips", "Devices & Graphs", "Misc"
                    ];

                    for category in categories {
                        egui::CollapsingHeader::new(category).default_open(true).show(ui, |ui| {
                            ui.horizontal_wrapped(|ui| {
                                for color_node in &mut active_skin.colors {
                                    if categorize_color(&color_node.name) == category {
                                        ui.allocate_ui(egui::vec2(220.0, 24.0), |ui| {
                                            ui.horizontal(|ui| {
                                                ui.set_width(220.0);
                                                let mut rgba = [
                                                    color_node.r as f32 / 255.0,
                                                    color_node.g as f32 / 255.0,
                                                    color_node.b as f32 / 255.0,
                                                    color_node.alpha as f32 / 255.0,
                                                ];
                                                if ui.color_edit_button_rgba_unmultiplied(&mut rgba).changed() {
                                                    color_node.r = (rgba[0] * 255.0).round() as u8;
                                                    color_node.g = (rgba[1] * 255.0).round() as u8;
                                                    color_node.b = (rgba[2] * 255.0).round() as u8;
                                                    color_node.alpha = (rgba[3] * 255.0).round() as u8;
                                                    any_changed = true;
                                                }
                                                ui.add(egui::Label::new(&color_node.name).truncate());
                                            });
                                        });
                                    }
                                }
                            });
                        });
                    }

                    if any_changed {
                        active_skin.sync_cache();
                    }

                    ui.add_space(10.0);
                    if ui.button("Save modified.ask").clicked() {
                        active_skin.update_xml();
                        let xml_out = active_skin.to_xml_string();
                        let _ = std::fs::write("modified.ask", xml_out);
                    }

                    // --- ALL COLOR SWATCHES ---
                    ui.add_space(30.0);
                    egui::CollapsingHeader::new(egui::RichText::new("Full Palette Reference").heading())
                        .default_open(false)
                        .show(ui, |ui| {
                            ui.add_space(10.0);
                            for category in categories {
                                let has_colors = active_skin.colors.iter().any(|c| categorize_color(&c.name) == category);
                                
                                if has_colors {
                                    ui.label(egui::RichText::new(category).strong());
                                    ui.add_space(5.0);
                                    
                                    ui.horizontal_wrapped(|ui| {
                                        for color_node in &active_skin.colors {
                                            if categorize_color(&color_node.name) == category {
                                                let col = egui::Color32::from_rgba_unmultiplied(color_node.r, color_node.g, color_node.b, color_node.alpha);
                                                
                                                ui.allocate_ui(egui::vec2(200.0, 24.0), |ui| {
                                                    ui.horizontal(|ui| {
                                                        ui.set_width(200.0);
                                                        let (rect, _) = ui.allocate_exact_size(egui::vec2(16.0, 16.0), egui::Sense::hover());
                                                        ui.painter().rect_filled(rect, 2.0, col);
                                                        ui.painter().rect_stroke(rect, 0.0, (1.0, egui::Color32::from_gray(100)), egui::StrokeKind::Outside);
                                                        
                                                        ui.add(egui::Label::new(&color_node.name).truncate());
                                                    });
                                                });
                                            }
                                        }
                                    });
                                    ui.add_space(10.0);
                                }
                            }
                        });
                } else {
                    ui.label("No skin loaded yet...");
                }
            });
        });
    }

    fn draw_preview(&mut self, ui: &mut egui::Ui) {
        ui.push_id("preview_scroll", |ui| {
            egui::ScrollArea::both().auto_shrink([false; 2]).show(ui, |ui| {
            
            let get_col = |name: &str, fallback: egui::Color32| -> egui::Color32 {
                self.active_skin.as_ref()
                    .and_then(|s| s.get_color(name))
                    .unwrap_or(fallback)
            };

            let surface_bg = get_col("SurfaceBackground", egui::Color32::from_gray(40));
            let surface_area = get_col("SurfaceArea", egui::Color32::from_gray(50));
            let control_bg = get_col("ControlBackground", egui::Color32::from_gray(60));
            let text_color = get_col("ViewControlOff", egui::Color32::WHITE);
            let browser_bg = get_col("BrowserBar", egui::Color32::from_gray(30));
            let transport_bg = get_col("TransportBackground", egui::Color32::from_gray(20));
            let detail_bg = get_col("DetailViewBackground", surface_area);
            let device_bg = get_col("SurfaceAreaFocus", control_bg);
            
            let track_activator = get_col("ViewCheckControlEnabledOn", egui::Color32::from_rgb(255, 180, 0));
            let track_activator_off = get_col("ViewCheckControlEnabledOff", egui::Color32::from_gray(100));
            
            let clip_1 = get_col("Clip1", egui::Color32::from_rgb(0, 200, 200));
            let clip_2 = get_col("Clip2", egui::Color32::from_rgb(0, 200, 0));
            let clip_3 = get_col("Clip3", egui::Color32::from_rgb(0, 0, 200));
            let clip_4 = get_col("Clip4", egui::Color32::from_rgb(200, 0, 200));
            let graph_color = get_col("ThresholdLineColor", egui::Color32::from_rgb(0, 200, 255));
            let env_color = get_col("RetroDisplayGreen", egui::Color32::from_rgb(0, 255, 100));
            let meter_normal = get_col("MeterLevelNormal", egui::Color32::from_rgb(0, 200, 0));
            let meter_high = get_col("MeterLevelHigh", egui::Color32::from_rgb(255, 200, 0));
            let meter_peak = get_col("MeterLevelLow", egui::Color32::from_rgb(255, 0, 0)); // Low actually implies peak in some contexts or vice versa, but we'll use peak color

            egui::Frame::new()
                .fill(surface_bg)
                .inner_margin(8.0)
                .show(ui, |ui| {
                    ui.style_mut().visuals.override_text_color = Some(text_color);

                    // Top Bar
                    egui::Frame::new().fill(transport_bg).inner_margin(4.0).show(ui, |ui| {
                        ui.horizontal(|ui| {
                            ui.label("Link");
                            ui.label("TAP");
                            ui.label("120.00");
                            ui.separator();
                            ui.label("4 / 4");
                            ui.separator();
                            ui.label("OVR");
                            ui.separator();
                            let _ = ui.button("▶");
                            let _ = ui.button("■");
                            let _ = ui.button("⏺");
                            ui.separator();
                            ui.label("1. 1. 1");
                            ui.separator();
                            ui.label(egui::RichText::new("KEY").color(track_activator));
                            ui.label(egui::RichText::new("MIDI").color(text_color));
                        });
                    });

                    ui.add_space(8.0);

                    // Main Area
                    ui.horizontal(|ui| {
                        // Browser
                        egui::Frame::new().fill(browser_bg).inner_margin(4.0).show(ui, |ui| {
                            ui.set_width(120.0);
                            ui.vertical(|ui| {
                                ui.heading("Collections");
                                ui.label(egui::RichText::new("🔴 Favorites").color(get_col("BrowserActiveItem", text_color)));
                                ui.label(egui::RichText::new("🟠 Synths").color(text_color));
                                ui.label(egui::RichText::new("🟡 Drums").color(text_color));
                                ui.add_space(10.0);
                                ui.heading("Library");
                                ui.label("🎵 Sounds");
                                ui.label("🎹 Instruments");
                                ui.label("🎛 Audio Effects");
                                ui.label("🎼 MIDI Effects");
                                ui.label("🎸 Plug-ins");
                                ui.label("📂 Samples");
                            });
                        });

                        ui.add_space(8.0);

                        // Right Side (Session + Details)
                        ui.vertical(|ui| {
                            // Session View
                            egui::Frame::new().fill(surface_area).inner_margin(4.0).show(ui, |ui| {
                                let available_h = ui.available_height();
                                ui.set_height(available_h * 0.6); // 60% of vertical space
                                
                                ui.horizontal(|ui| {
                                    let tracks = [
                                        ("1 Lead", clip_1, 0.7, true),
                                        ("2 Pad", clip_2, 0.4, true),
                                        ("3 Bass", clip_3, 0.8, false),
                                        ("4 Drums", clip_4, 0.9, true),
                                    ];
                                    
                                    for (i, (name, color, vol, on)) in tracks.iter().enumerate() {
                                        ui.push_id(i, |ui| {
                                            ui.vertical(|ui| {
                                                ui.set_width(70.0);
                                                // Track Header
                                                egui::Frame::new().fill(*color).inner_margin(4.0).show(ui, |ui| {
                                                    ui.label(egui::RichText::new(*name).color(egui::Color32::BLACK));
                                                });
                                                ui.add_space(2.0);
                                                // Clip Slots
                                                for j in 0..6 {
                                                    egui::Frame::new().fill(if j == 0 && *on { *color } else { control_bg }).inner_margin(6.0).show(ui, |ui| {
                                                        if j == 0 && *on {
                                                            ui.label(egui::RichText::new("▶").color(egui::Color32::BLACK));
                                                        } else {
                                                            ui.label("");
                                                        }
                                                    });
                                                    ui.add_space(2.0);
                                                }
                                                ui.add_space(10.0);
                                                // Mixer Section
                                                ui.label("Sends");
                                                ui.add(egui::Slider::new(&mut 0.0, 0.0..=1.0).show_value(false));
                                                ui.add_space(5.0);
                                                ui.label("Pan");
                                                ui.add(egui::Slider::new(&mut 0.5, 0.0..=1.0).show_value(false));
                                                ui.add_space(5.0);
                                                
                                                // Track Activator & Solo/Arm
                                                ui.horizontal(|ui| {
                                                    egui::Frame::new().fill(if *on { track_activator } else { track_activator_off }).inner_margin(4.0).show(ui, |ui| {
                                                        ui.colored_label(egui::Color32::BLACK, format!("{}", i + 1));
                                                    });
                                                    ui.label("S");
                                                    ui.label("⏺");
                                                });

                                                ui.add_space(5.0);

                                                // Volume Fader & Meter
                                                ui.horizontal(|ui| {
                                                    let (meter_rect, _) = ui.allocate_exact_size(egui::vec2(10.0, 60.0), egui::Sense::hover());
                                                    ui.painter().rect_filled(meter_rect, 0.0, control_bg);
                                                    let meter_h = 60.0 * (*vol);
                                                    let level_rect = egui::Rect::from_min_size(
                                                        meter_rect.left_bottom() - egui::vec2(0.0, meter_h),
                                                        egui::vec2(10.0, meter_h)
                                                    );
                                                    let level_col = if *vol > 0.8 { meter_peak } else if *vol > 0.6 { meter_high } else { meter_normal };
                                                    ui.painter().rect_filled(level_rect, 0.0, level_col);
                                                    
                                                    ui.add(egui::Slider::new(&mut (*vol as f64), 0.0..=1.0).vertical().show_value(false));
                                                });
                                            });
                                        });
                                        ui.separator();
                                    }

                                    // Return Tracks and Master
                                    ui.vertical(|ui| {
                                        ui.set_width(70.0);
                                        egui::Frame::new().fill(control_bg).inner_margin(4.0).show(ui, |ui| {
                                            ui.label("A Reverb");
                                        });
                                        ui.add_space(150.0); // skip clip slots
                                        ui.label("Sends");
                                        ui.add(egui::Slider::new(&mut 0.0, 0.0..=1.0).show_value(false));
                                        ui.label("Pan");
                                        ui.add(egui::Slider::new(&mut 0.5, 0.0..=1.0).show_value(false));
                                    });
                                    
                                    ui.separator();

                                    ui.vertical(|ui| {
                                        ui.set_width(70.0);
                                        egui::Frame::new().fill(get_col("MasterTrackTitle", control_bg)).inner_margin(4.0).show(ui, |ui| {
                                            ui.label("Master");
                                        });
                                        ui.add_space(2.0);
                                        // Scene Launch
                                        for k in 1..=6 {
                                            egui::Frame::new().fill(control_bg).inner_margin(6.0).show(ui, |ui| {
                                                ui.label(format!("▶ {}", k));
                                            });
                                            ui.add_space(2.0);
                                        }
                                        ui.add_space(10.0);
                                        ui.label("Pan");
                                        ui.add(egui::Slider::new(&mut 0.5, 0.0..=1.0).show_value(false));
                                        ui.add_space(10.0);
                                        // Master Fader
                                        ui.horizontal(|ui| {
                                            let (meter_rect, _) = ui.allocate_exact_size(egui::vec2(16.0, 80.0), egui::Sense::hover());
                                            ui.painter().rect_filled(meter_rect, 0.0, control_bg);
                                            let meter_h = 80.0 * 0.85;
                                            let level_rect = egui::Rect::from_min_size(
                                                meter_rect.left_bottom() - egui::vec2(0.0, meter_h),
                                                egui::vec2(16.0, meter_h)
                                            );
                                            ui.painter().rect_filled(level_rect, 0.0, meter_normal);
                                            
                                            ui.add(egui::Slider::new(&mut 0.85, 0.0..=1.0).vertical().show_value(false));
                                        });
                                    });
                                });
                            });

                            ui.add_space(8.0);

                            // Detail View / Devices
                            egui::Frame::new().fill(detail_bg).inner_margin(8.0).show(ui, |ui| {
                                ui.set_width(ui.available_width());
                                ui.set_height(ui.available_height());
                                
                                ui.horizontal(|ui| {
                                    // Wavetable Device Mockup
                                    egui::Frame::new().fill(device_bg).inner_margin(6.0).show(ui, |ui| {
                                        ui.vertical(|ui| {
                                            ui.label("Wavetable");
                                            ui.separator();
                                            ui.horizontal(|ui| {
                                                ui.vertical(|ui| {
                                                    ui.label("Osc 1");
                                                    let (rect, _resp) = ui.allocate_exact_size(egui::vec2(80.0, 40.0), egui::Sense::hover());
                                                    ui.painter().rect_stroke(rect, 0.0, (1.0, graph_color), egui::StrokeKind::Inside);
                                                    ui.painter().line_segment([rect.left_center(), rect.right_top()], (2.0, graph_color));
                                                });
                                                ui.vertical(|ui| {
                                                    ui.label("Amp Env");
                                                    let (rect, _resp) = ui.allocate_exact_size(egui::vec2(80.0, 40.0), egui::Sense::hover());
                                                    ui.painter().rect_stroke(rect, 0.0, (1.0, env_color), egui::StrokeKind::Inside);
                                                    // Draw an envelope shape
                                                    ui.painter().line_segment([rect.left_bottom(), rect.center_top()], (2.0, env_color));
                                                    ui.painter().line_segment([rect.center_top(), rect.right_center()], (2.0, env_color));
                                                });
                                            });
                                        });
                                    });

                                    ui.add_space(10.0);

                                    // EQ Eight Mockup
                                    egui::Frame::new().fill(device_bg).inner_margin(6.0).show(ui, |ui| {
                                        ui.vertical(|ui| {
                                            ui.label("EQ Eight");
                                            ui.separator();
                                            let (rect, _resp) = ui.allocate_exact_size(egui::vec2(120.0, 60.0), egui::Sense::hover());
                                            ui.painter().rect_filled(rect, 0.0, control_bg);
                                            // Draw EQ curve
                                            ui.painter().line_segment([rect.left_center(), rect.center()], (2.0, graph_color));
                                            ui.painter().line_segment([rect.center(), rect.right_bottom()], (2.0, graph_color));
                                        });
                                    });
                                });
                            });
                        });
                });
            });
        });
        });
    }
}

fn main() -> eframe::Result<()> {
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default()
            .with_inner_size([1200.0, 900.0])
            .with_min_inner_size([900.0, 700.0]),
        ..Default::default()
    };
    eframe::run_native(
        "Colour Ableton Live 12",
        options,
        Box::new(|_cc| Ok(Box::new(MyApp::default()))),
    )
}
