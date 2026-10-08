# colour-ableton-live-12
A native application used to customize the appearance of Ableton Live 12 skins (`.ask` files). (WIP)

## Architecture
The project has been rewritten from its original Python script proof-of-concept into a lightweight, highly-performant native desktop application built with **Rust**. 

### Key Technologies
- **egui / eframe:** Provides the fast, immediate-mode GUI for the desktop application, compiling to a tiny standalone executable for both Windows and Mac.
- **axum & tokio:** An embedded asynchronous web server. This can be optionally enabled from the desktop UI to host a premium web-based frontend or provide a local API for remote access.
- **quick-xml:** For blazing-fast parsing and serialization of Ableton's XML-based `.ask` format.

## Current Status
The project is currently in the scaffolding phase. The native Rust UI compiles and runs, and the embedded web server can be successfully toggled on/off. 

## Next Steps
The following core features are planned for implementation:
- **XML Parsing:** Implement `quick-xml` to read `.ask` files and convert the nested `<R>`, `<G>`, `<B>`, `<Alpha>` structure into a flat hex-based struct.
- **Color Editor UI:** Build the visual color picker within the `egui` interface to allow users to interact with the parsed colors.
- **Live Replica UI:** Generate a rescalable, live replica of the Ableton Live 12 UI inside the main window (with color settings on the side/below) to instantly preview color changes.
- **Reverse Conversion & Export:** Implement functionality to convert modified Hex values back into the Ableton XML structure and save the new `.ask` file.
- **Web Frontend (Optional):** Serve a rich HTML/CSS/JS frontend via the embedded `axum` server to provide a premium, dynamic web UI.

## Building and Running
Ensure you have [Rust and Cargo installed](https://rustup.rs/).
```bash
# Run the desktop application
cargo run
```
