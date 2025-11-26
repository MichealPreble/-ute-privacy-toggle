import os
import sys
import subprocess
from openai import OpenAI

# --- CONFIGURATION ---
API_KEY = os.getenv("OPENAI_API_KEY")  # Ensure this is set in your terminal
CLIENT = OpenAI(api_key=API_KEY)

SYSTEM_PROMPT = """
You are a Senior iOS Engineer and DevOps Specialist.
Your goal is to scaffold a production-ready SwiftUI app based on a user idea.

You must output THREE things separated by distinct markers:
1. The `project.yml` file content (for XcodeGen).
2. The `ContentView.swift` code.
3. The `App.swift` code.

**RULES FOR project.yml:**
- Target iOS 17.0.
- Use strict indentation (YAML).
- Include standard `info` plist keys (UILaunchScreen, UISupportedInterfaceOrientations).
- Add a specific 'deploymentTarget' section.
- PRODUCT_BUNDLE_IDENTIFIER should be 'com.yourname.[appname_sanitized]'.
- ENABLE_PREVIEWS: YES.

**RULES FOR SWIFT CODE:**
- Use modern SwiftUI (Observation, SwiftData if needed).
- Ensure the code compiles without external dependencies if possible, or use standard Apple frameworks.
- Make the UI look "Apple Design" quality (clean, whitespace, SF Symbols).

**OUTPUT FORMAT:**
---PROJECT_YML---
(YAML content here)
---CONTENT_VIEW---
(Swift code here)
---APP_SWIFT---
(Swift code here)
"""

def generate_ios_project(app_idea: str) -> str:
    print(f"\ud83d\udcf1 Architecting iOS App: '{app_idea}'...")
    print("\u23f3 Asking AI to write the configuration and code...")

    try:
        response = CLIENT.chat.completions.create(
            model="gpt-4o",  # Use 4o or 3.5-sonnet for best code capability
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Build a SwiftUI app for: {app_idea}"},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"\u274c Error: {e}")
        sys.exit(1)


def save_files(project_name: str, content: str) -> str:
    # Parse the content based on markers
    try:
        parts = content.split("---PROJECT_YML---")[1].split("---CONTENT_VIEW---")
        project_yml = parts[0].strip()

        parts2 = parts[1].split("---APP_SWIFT---")
        content_view = parts2[0].strip()
        app_swift = parts2[1].strip()
    except IndexError:
        print("\u274c AI failed to format the response correctly. Try again.")
        sys.exit(1)

    # Create Directory Structure
    base_dir = project_name.replace(" ", "")
    source_dir = os.path.join(base_dir, project_name.replace(" ", ""))

    os.makedirs(source_dir, exist_ok=True)

    # Write project.yml
    with open(os.path.join(base_dir, "project.yml"), "w", encoding="utf-8") as f:
        f.write(project_yml)

    # Write Swift Files
    with open(os.path.join(source_dir, "ContentView.swift"), "w", encoding="utf-8") as f:
        f.write(content_view)

    with open(
        os.path.join(source_dir, f"{project_name.replace(' ', '')}App.swift"),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(app_swift)

    print(f"\n\ud83d\udcc2 Created folder: {base_dir}/")
    return base_dir


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python ios_builder.py 'Your App Idea'")
        sys.exit(1)

    app_idea = sys.argv[1]
    raw_output = generate_ios_project(app_idea)

    # We'll use a generic name for the folder or try to extract it,
    # but for simplicity let's call it "GeneratedApp"
    project_dir = save_files("GeneratedApp", raw_output)

    print("\n\u2705 GENERATION COMPLETE.")
    print("\ud83d\udc49 To finish building the Xcode project, run these commands:")
    print(f"   cd {project_dir}")
    print("   xcodegen generate")
    print("   open GeneratedApp.xcodeproj")


if __name__ == "__main__":
    main()
