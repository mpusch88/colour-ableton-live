use std::str::FromStr;
use xmltree::Element;

#[derive(Debug, Clone)]
pub struct ColorNode {
    pub name: String,
    pub r: u8,
    pub g: u8,
    pub b: u8,
    pub alpha: u8,
}

pub struct Skin {
    pub root: Element,
    pub colors: Vec<ColorNode>,
    color_map: std::collections::HashMap<String, eframe::egui::Color32>,
}

impl Skin {
    pub fn parse(xml: &str) -> Result<Self, xmltree::ParseError> {
        let root = Element::parse(xml.as_bytes())?;
        let mut colors = Vec::new();

        if let Some(skin_manager) = root.get_child("SkinManager") {
            for child in &skin_manager.children {
                if let xmltree::XMLNode::Element(elem) = child {
                    if elem.get_child("R").is_some()
                        && elem.get_child("G").is_some()
                        && elem.get_child("B").is_some()
                        && elem.get_child("Alpha").is_some()
                    {
                        let r = parse_value_attr(elem.get_child("R").unwrap());
                        let g = parse_value_attr(elem.get_child("G").unwrap());
                        let b = parse_value_attr(elem.get_child("B").unwrap());
                        let alpha = parse_value_attr(elem.get_child("Alpha").unwrap());

                        colors.push(ColorNode {
                            name: elem.name.clone(),
                            r,
                            g,
                            b,
                            alpha,
                        });
                    }
                }
            }
        }

        let mut skin = Self {
            root,
            colors,
            color_map: std::collections::HashMap::new(),
        };
        skin.sync_cache();
        Ok(skin)
    }

    pub fn sync_cache(&mut self) {
        self.color_map.clear();
        for c in &self.colors {
            self.color_map.insert(
                c.name.clone(),
                eframe::egui::Color32::from_rgba_unmultiplied(c.r, c.g, c.b, c.alpha),
            );
        }
    }

    pub fn update_xml(&mut self) {
        if let Some(skin_manager) = self.root.get_mut_child("SkinManager") {
            for color_node in &self.colors {
                if let Some(child) = skin_manager.get_mut_child(color_node.name.as_str()) {
                    if let Some(r) = child.get_mut_child("R") {
                        set_value_attr(r, color_node.r);
                    }
                    if let Some(g) = child.get_mut_child("G") {
                        set_value_attr(g, color_node.g);
                    }
                    if let Some(b) = child.get_mut_child("B") {
                        set_value_attr(b, color_node.b);
                    }
                    if let Some(a) = child.get_mut_child("Alpha") {
                        set_value_attr(a, color_node.alpha);
                    }
                }
            }
        }
    }

    pub fn to_xml_string(&self) -> String {
        let mut out = Vec::new();
        let config = xmltree::EmitterConfig::new()
            .perform_indent(true)
            .pad_self_closing(true);
        self.root.write_with_config(&mut out, config).unwrap();
        String::from_utf8(out).unwrap()
    }

    pub fn get_color(&self, name: &str) -> Option<eframe::egui::Color32> {
        self.color_map.get(name).copied()
    }
}

fn parse_value_attr(element: &Element) -> u8 {
    element.attributes.get("Value").and_then(|v| u8::from_str(v).ok()).unwrap_or(0)
}

fn set_value_attr(element: &mut Element, value: u8) {
    element.attributes.insert("Value".to_string(), value.to_string());
}
