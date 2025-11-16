# RSD Floaty v0.1 — Code & Deployment Playbook

This document is the single source of truth for assembling, running, and shipping the RSD Floaty MVP to TestFlight. Paste the code blocks into the corresponding Swift files inside an iOS 17+ SwiftUI project, then follow the integration steps below.

---

## 1. Final Code (Copy/Paste Ready)

### RSDFloatyApp.swift
```swift
import SwiftUI
import SwiftData

@main
struct RSDFloatyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: FloatySession.self)
    }
}
```

### FloatySession.swift
```swift
import Foundation
import SwiftData

@Model
final class FloatySession: Identifiable {
    var timestamp: Date
    var intensity: Int
    var feltHelped: Bool?
    var note: String

    init(intensity: Int, feltHelped: Bool?, note: String, timestamp: Date = .now) {
        self.intensity = intensity
        self.feltHelped = feltHelped
        self.note = note
        self.timestamp = timestamp
    }
}
```

### ContentView.swift
```swift
import SwiftUI
import SwiftData

struct ContentView: View {
    @Environment(\.modelContext) private var context
    @Query(sort: \FloatySession.timestamp, order: .reverse) private var sessions: [FloatySession]
    @State private var isPresentingSession = false

    var body: some View {
        NavigationStack {
            VStack(spacing: 24) {
                Button {
                    isPresentingSession = true
                } label: {
                    VStack(spacing: 8) {
                        Text("I'm overwhelmed")
                            .font(.title2.weight(.semibold))
                        Text("Tap to start a Floaty. 30 seconds. No judgment.")
                            .font(.subheadline)
                            .foregroundStyle(.secondary)
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.accentColor.opacity(0.1))
                    .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))
                }
                .buttonStyle(.plain)

                if sessions.isEmpty {
                    ContentUnavailableView(
                        "No Floaties yet",
                        systemImage: "sparkles",
                        description: Text("When a spike hits, tap the button above. Future-you will see the receipts.")
                    )
                } else {
                    List {
                        ForEach(sessions) { session in
                            VStack(alignment: .leading, spacing: 6) {
                                HStack {
                                    Text("Intensity \(session.intensity)/10")
                                        .font(.headline)
                                    Spacer()
                                    Text(session.timestamp, style: .date)
                                        .font(.caption)
                                        .foregroundStyle(.secondary)
                                }

                                if let feltHelped = session.feltHelped {
                                    Text(feltHelped ? "Helped a bit" : "Not really sure")
                                        .font(.subheadline)
                                }

                                if !session.note.isEmpty {
                                    Text(session.note)
                                        .font(.footnote)
                                        .foregroundStyle(.secondary)
                                }
                            }
                            .padding(.vertical, 6)
                        }
                        .onDelete(perform: deleteSessions)
                    }
                }
            }
            .padding()
            .navigationTitle("RSD Floaty")
            .toolbar { EditButton() }
        }
        .sheet(isPresented: $isPresentingSession) {
            FloatySessionView { session in
                context.insert(session)
                try? context.save()
            }
        }
    }

    private func deleteSessions(at offsets: IndexSet) {
        for index in offsets {
            context.delete(sessions[index])
        }
        try? context.save()
    }
}
```

### FloatySessionView.swift
```swift
import SwiftUI

struct FloatySessionView: View {
    @Environment(\.dismiss) private var dismiss

    @State private var intensity: Double = 7
    @State private var feltHelped: Bool? = nil
    @State private var note: String = ""

    let onSave: (FloatySession) -> Void

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 16) {
                    Group {
                        Text("RSD Floaty")
                            .font(.title2.weight(.semibold))
                        Text("This looks like a big feelings spike.\nYour nervous system is loud right now — that doesn't mean the story in your head is true.")
                            .font(.subheadline)
                            .foregroundStyle(.secondary)
                    }
                    .padding(.bottom, 8)

                    Divider()

                    Group {
                        Text("Step 1 · Body first (30–60 sec)")
                            .font(.headline)

                        Text("Pick ONE to try:")
                            .font(.subheadline)

                        VStack(alignment: .leading, spacing: 8) {
                            Text("• 4–6 breathing: In through nose for 4, out through mouth for 6. Do this 6 times.")
                            Text("• Or: Cold water on wrists / face for 20–30 seconds.")
                            Text("• Or: Feet flat on floor, press down hard for 10 seconds, release, repeat 3 times.")
                        }
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                    }

                    Divider()

                    Group {
                        Text("Step 2 · How strong is it?")
                            .font(.headline)
                        HStack {
                            Text("1")
                            Slider(value: $intensity, in: 1...10, step: 1)
                            Text("10")
                        }
                        Text("Gut feeling is fine. You chose \(Int(intensity)) / 10.")
                            .font(.footnote)
                            .foregroundStyle(.secondary)

                        if Int(intensity) >= 9 {
                            Text("If you feel unsafe or like you might hurt yourself, this app isn't enough. Please reach out to a trusted person or local crisis line if you can.")
                                .font(.footnote)
                                .foregroundStyle(.red)
                        }
                    }

                    Divider()

                    Group {
                        Text("Step 3 · Did this help even a little?")
                            .font(.headline)

                        HStack {
                            Button {
                                feltHelped = true
                            } label: {
                                Label("Helped a bit", systemImage: feltHelped == true ? "hand.thumbsup.fill" : "hand.thumbsup")
                            }
                            .buttonStyle(.bordered)

                            Button {
                                feltHelped = false
                            } label: {
                                Label("Not really sure", systemImage: feltHelped == false ? "questionmark.circle.fill" : "questionmark.circle")
                            }
                            .buttonStyle(.bordered)
                        }
                        .font(.subheadline)
                    }

                    Divider()

                    Group {
                        Text("Optional · Note for future you / therapist")
                            .font(.headline)
                        Text("1–2 sentences is plenty. Example: \"Boss said I was too intense in the meeting and I shut down.\"")
                            .font(.footnote)
                            .foregroundStyle(.secondary)

                        TextEditor(text: $note)
                            .frame(minHeight: 100)
                            .overlay(
                                RoundedRectangle(cornerRadius: 12)
                                    .stroke(Color.secondary.opacity(0.3), lineWidth: 1)
                            )

                        Text("This moment sucks. The fact you opened this and got this far already counts.")
                            .font(.footnote)
                            .foregroundStyle(.secondary)
                    }
                }
                .padding()
            }
            .navigationTitle("Floaty Session")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Close") { dismiss() }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Save") {
                        let session = FloatySession(
                            intensity: Int(intensity),
                            feltHelped: feltHelped,
                            note: note.trimmingCharacters(in: .whitespacesAndNewlines)
                        )
                        onSave(session)
                        dismiss()
                    }
                }
            }
        }
    }
}
```

---

## 2. Xcode Integration Checklist

1. **Create the project** — Xcode → File → New → Project → *App*. Name it `RSDFloaty`, Interface `SwiftUI`, Language `Swift`, enable SwiftData (iOS 17+ target).
2. **Add files** — Replace the template files with the code blocks above (four files total). Delete ContentView.swift/App.swift generated by the template before adding the new versions.
3. **Assets** — Optional, but set an app icon (even a placeholder) so TestFlight accepts the build.
4. **Build settings** — Set deployment target to iOS 17.0 or higher.

---

## 3. Run on Device (Pre-TestFlight)

1. Plug in your iPhone and trust the computer if prompted.
2. In Xcode, pick your iPhone from the run destination menu.
3. Go to *Signing & Capabilities* → choose your Apple ID team and set a unique bundle identifier (`com.yourname.rsdfloaty`).
4. Press **⌘R**. On first launch, approve the developer certificate on the phone (Settings → General → VPN & Device Management).
5. Complete one real Floaty session to confirm data saves locally.

---

## 4. Ship to TestFlight

1. **Archive** — Product → Archive with a Release configuration.
2. **Distribute** — In the Organizer, choose *Distribute App* → App Store Connect → Upload.
3. **App Store Connect** — Create the app record (name, bundle ID, platform iOS). Add a privacy policy link (can be a placeholder Google Doc for internal TestFlight).
4. **Test Information** — Describe what the app does, note that all data is stored locally (no analytics).
5. **Submit for review** — Internal testing is usually approved in minutes. Add your personal Apple ID as the first tester.

---

## 5. Guardrails & Evidence Rules

- **No claims without receipts** — Any future patent or marketing statement must cite logs, data exports, or session anonymized evidence captured via SwiftData.
- **Local-only v0.1** — Keep the “no network, no analytics” promise to maintain user trust during initial counseling/testing.
- **Crisis messaging** — Do not alter the high-intensity warning without legal review.

---

Once you complete one real spike with this build, RSD Floaty v0.1 is officially shipped. Iterate only after that lived experience check-in.
