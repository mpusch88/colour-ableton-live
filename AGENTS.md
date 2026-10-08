# Colour Ableton Live 12 - Agent Guidelines

Welcome to the `colour-ableton-live` repository. This is a Rust-based desktop application built using the `egui` framework and `eframe` for editing Ableton Live 12 skin files (`.ask` XML).

## 1. Technology Stack
- **Rust**: Primary language.
- **egui / eframe**: Immediate mode GUI framework used for all rendering and layouts.
- **axum / tokio**: Used for the backend web server API (remote control).
- **xmltree**: Used for safely parsing and writing the `.ask` XML skin files.

## 2. Development & Layout Rules
- **egui Layout Quirks**: When nesting `ScrollArea` inside dynamic containers like `ui.horizontal`, always explicitly pass pre-calculated dimensions (e.g., using `ui.available_height()`) to `allocate_ui_with_layout` to prevent the UI from collapsing into 0-height slivers.
- **Widget IDs**: When generating multiple widgets dynamically (e.g., in loops for the UI preview tracks), always wrap them in `ui.push_id(id, |ui| { ... })` to prevent `egui` ID collisions and interaction bugs.
- **Color Parsing**: Colors from the `.ask` file are categorized logically. Maintain the `categorize_color` logic when adding new mock UI elements.

## 3. General Workflow
- **Cargo Run Issues**: Orphaned `.exe` processes can sometimes cause "Access Denied" errors during compilation. If this occurs, kill the existing process before recompiling.
- **Web Server Component**: This application includes an embedded web server for remote control. Ensure `tokio` features and `axum` routes don't block the immediate mode GUI thread.
