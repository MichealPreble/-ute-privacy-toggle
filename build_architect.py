import os
import sys
from openai import OpenAI


API_KEY = os.getenv("OPENAI_API_KEY")


def load_system_prompt() -> str:
    """Load the architect system prompt from disk."""
    try:
        with open("architect_prompt.txt", "r", encoding="utf-8") as prompt_file:
            return prompt_file.read()
    except FileNotFoundError:
        print("❌ Error: 'architect_prompt.txt' not found.")
        print("   Please save the prompt text from Phase 1 into this file.")
        sys.exit(1)


def generate_build_plan(app_idea: str, client: OpenAI) -> str:
    """Send the idea to the Architect AI and return the generated build plan."""
    print(f"\n🧠 The Architect is analyzing: '{app_idea}'...")
    print("🏗️  Drafting database schema...")
    print("📝  Structuring implementation steps...")

    system_prompt = load_system_prompt()

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"APP IDEA: {app_idea}"},
            ],
            temperature=0.2,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"❌ API Error: {exc}")
        sys.exit(1)

    return response.choices[0].message.content


def main() -> None:
    print("--- 🕵️  SECRET BUILD PLAN GENERATOR 🕵️  ---")

    if not API_KEY:
        print("❌ Error: OPENAI_API_KEY not found in environment variables.")
        print("   Please run: export OPENAI_API_KEY='your-key-here'")
        sys.exit(1)

    client = OpenAI(api_key=API_KEY)

    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = input("👉 Describe your app idea: ")

    if not user_input.strip():
        print("❌ Please provide an idea.")
        return

    plan = generate_build_plan(user_input, client)

    filename = "BUILD_PLAN.md"
    with open(filename, "w", encoding="utf-8") as output_file:
        output_file.write(plan)

    print(f"\n✅ Success! Your secret blueprint is ready: {filename}")
    print("🚀 Next Step: Open this file and feed 'Step 1' to Cursor/Bolt.")


if __name__ == "__main__":
    main()
