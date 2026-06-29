"""
utils/ai_processor.py
Calls the Anthropic API to analyse meeting notes and return structured JSON.
"""
import os
import json
import anthropic

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a professional meeting analyst. 
Given raw meeting notes or a transcript, you extract structured information and return ONLY valid JSON — no markdown, no extra text.

The JSON schema:
{
  "summary": "string — the meeting summary (length/style per instruction)",
  "key_decisions": ["string", ...],
  "action_items": [
    {
      "task": "string",
      "owner": "string or null",
      "due_date": "string or null",
      "priority": "high | medium | low"
    }
  ],
  "deadlines": [
    {
      "item": "string",
      "date": "string",
      "owner": "string or null"
    }
  ],
  "people": [
    {
      "name": "string",
      "role": "string or null",
      "tasks": ["string", ...]
    }
  ]
}

Priority rules:
- high   = must-do, urgent, or explicitly flagged
- medium = normal task
- low    = nice-to-have / backlog
"""

LENGTH_INSTRUCTIONS = {
    "Brief":                  "Write a 3-to-5 bullet-point summary. Each bullet max 15 words.",
    "Standard":               "Write a single cohesive paragraph (5–8 sentences).",
    "Executive (Detailed)":   "Write a detailed executive summary with sections: Overview, Discussion Points, Outcomes. Use clear prose, 3–5 sentences per section.",
}


def process_meeting_notes(raw_text: str, summary_length: str, language: str = "English") -> dict:
    """Send meeting text to Claude and return parsed structured data."""

    length_instruction = LENGTH_INSTRUCTIONS.get(summary_length, LENGTH_INSTRUCTIONS["Standard"])
    lang_note = f"Write all output in {language}." if language != "English" else ""

    user_prompt = f"""Analyse the following meeting notes.

Summary instruction: {length_instruction}
{lang_note}

--- MEETING NOTES START ---
{raw_text[:12000]}
--- MEETING NOTES END ---

Return ONLY the JSON object. No explanation, no markdown fences."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )

        raw_json = response.content[0].text.strip()
        # Strip accidental markdown fences
        if raw_json.startswith("```"):
            raw_json = raw_json.split("```")[1]
            if raw_json.startswith("json"):
                raw_json = raw_json[4:]

        return json.loads(raw_json)

    except json.JSONDecodeError as e:
        return {"error": f"Could not parse AI response: {e}"}
    except Exception as e:
        return {"error": str(e)}
