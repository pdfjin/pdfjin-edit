import io
from pathlib import Path
from typing import List, Dict, Union
import pikepdf
from reportlab.pdfgen import canvas


def edit_pdf(input_pdf: Union[str, Path, bytes], edits: List[Dict], output: Union[str, Path] = None) -> bytes:
    src = pikepdf.open(str(input_pdf)) if isinstance(input_pdf, (str, Path)) else pikepdf.open(io.BytesIO(input_pdf))

    with src:
        for edit in edits:
            page_idx = edit.get("page", 0)
            if 0 <= page_idx < len(src.pages):
                page = src.pages[page_idx]
                w = float(page.mediabox[2] - page.mediabox[0])
                h = float(page.mediabox[3] - page.mediabox[1])

                packet = io.BytesIO()
                can = canvas.Canvas(packet, pagesize=(w, h))
                text = edit.get("text", "")
                x = edit.get("x", 50)
                y = edit.get("y", 50)
                size = edit.get("size", 12)
                can.setFont("Helvetica", size)
                can.drawString(x, y, text)
                can.save()
                packet.seek(0)
                with pikepdf.open(packet) as ov:
                    page.add_overlay(ov.pages[0])

        buf = io.BytesIO()
        src.save(buf)
        res = buf.getvalue()

    if output:
        Path(output).write_bytes(res)
    return res
