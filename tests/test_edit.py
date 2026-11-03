import io, pikepdf
from pdfjin_edit.core import edit_pdf


def test_edit():
    p = pikepdf.new()
    p.add_blank_page()
    buf = io.BytesIO()
    p.save(buf)
    res = edit_pdf(buf.getvalue(), [{"text": "Hello", "x": 10, "y": 10}])
    with pikepdf.open(io.BytesIO(res)) as doc:
        assert len(doc.pages) == 1
