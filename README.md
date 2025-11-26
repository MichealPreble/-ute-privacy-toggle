# iOS Architect: XcodeGen Scaffolder

This repository ships a small helper script (`ios_builder.py`) that turns an app idea into a ready-to-generate XcodeGen project scaffold. The script asks GPT-4o to produce `project.yml` plus starter SwiftUI sources so you can compile a clean `.xcodeproj` without hand-editing `project.pbxproj` files.

## Requirements
- macOS with Homebrew
- Xcode 15+ with the Xcode command line tools installed
- [XcodeGen](https://github.com/yonaskolb/XcodeGen):
  ```bash
  brew install xcodegen
  ```
- Python 3.10+ with the [`openai`](https://pypi.org/project/openai/) package installed
- An `OPENAI_API_KEY` environment variable configured in your shell

## Usage
1. Run the builder with your idea:
   ```bash
   python ios_builder.py "A simple crypto price tracker using mock data"
   ```
2. Move into the generated folder and create the Xcode project:
   ```bash
   cd GeneratedApp
   xcodegen generate
   open GeneratedApp.xcodeproj
   ```
3. In Xcode, select your team under **Signing & Capabilities** before archiving for TestFlight.

## How it works
`ios_builder.py` prompts the model with rules for a production-friendly SwiftUI target (iOS 17). It expects the AI response to include three marked sections for `project.yml`, `ContentView.swift`, and `App.swift`, writes them to `GeneratedApp/`, and prints the follow-up XcodeGen commands.
