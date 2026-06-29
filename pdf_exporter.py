"""
utils/pdf_exporter.py
Generates a clean PDF from the structured meeting analysis result.
"""
from datetime import datetime
from fpdf import FPDF


class MeetingPDF(FPDF):
    """Custom FPDF subclass with consistent header/footer."""

    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(15, 23, 42)   # slate-900
        self.cell(0, 10, "MeetingMind – Meeting Summary", align="L", ln=True)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(100, 116, 139)
        self.cell(0, 6, f"Generated {datetime.now().strftime('%B %d, %Y at %H:%M')}", ln=True)
        self.ln(4)
        self.set_draw_color(226, 232, 240)
        self.set_line_width(0.4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def section_title(self, title: str):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(15, 23, 42)
        self.set_fill_color(248, 250, 252)
        self.cell(0, 9, f"  {title}", ln=True, fill=True)
        self.ln(2)

    def body_text(self, text: str, indent: int = 0):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(51, 65, 85)
        self.set_x(10 + indent)
        self.multi_cell(0, 6, text)
        self.ln(1)

    def bullet(self, text: str, symbol: str = "•"):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(51, 65, 85)
        self.set_x(14)
        self.cell(6, 6, symbol)
        self.set_x(20)
        self.multi_cell(0, 6, text)


def export_summary_to_pdf(result: dict, raw_text: str, summary_length: str) -> bytes:
    """Build and return a PDF as bytes."""
    pdf = MeetingPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # ── Summary ───────────────────────────────────────────────────────────────
    pdf.section_title("📄 Summary")
    summary = result.get("summary", "No summary available.")
    pdf.body_text(summary)
    pdf.ln(4)

    # ── Key Decisions ─────────────────────────────────────────────────────────
    decisions = result.get("key_decisions", [])
    if decisions:
        pdf.section_title("🔑 Key Decisions")
        for d in decisions:
            pdf.bullet(d)
        pdf.ln(4)

    # ── Action Items ──────────────────────────────────────────────────────────
    actions = result.get("action_items", [])
    if actions:
        pdf.section_title("✅ Action Items")
        for i, item in enumerate(actions, 1):
            task  = item.get("task", "—")
            owner = item.get("owner") or "Unassigned"
            due   = item.get("due_date") or "No date"
            pri   = item.get("priority", "medium").capitalize()
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(15, 23, 42)
            pdf.set_x(14)
            pdf.cell(0, 7, f"{i}. {task}", ln=True)
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(100, 116, 139)
            pdf.set_x(20)
            pdf.cell(0, 5, f"Owner: {owner}   |   Due: {due}   |   Priority: {pri}", ln=True)
            pdf.ln(2)
        pdf.ln(2)

    # ── Deadlines ─────────────────────────────────────────────────────────────
    deadlines = result.get("deadlines", [])
    if deadlines:
        pdf.section_title("📅 Deadlines")
        for dl in deadlines:
            date  = dl.get("date", "TBD")
            item  = dl.get("item", "—")
            owner = dl.get("owner") or ""
            line  = f"{date}: {item}"
            if owner:
                line += f"  (Owner: {owner})"
            pdf.bullet(line, "▶")
        pdf.ln(4)

    # ── People ────────────────────────────────────────────────────────────────
    people = result.get("people", [])
    if people:
        pdf.section_title("👥 People & Responsibilities")
        for p in people:
            name  = p.get("name", "—")
            role  = p.get("role") or ""
            tasks = p.get("tasks", [])
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(15, 23, 42)
            pdf.set_x(14)
            heading = name if not role else f"{name} ({role})"
            pdf.cell(0, 7, heading, ln=True)
            for t in tasks:
                pdf.bullet(t, "–")
            pdf.ln(2)

    return bytes(pdf.output())
