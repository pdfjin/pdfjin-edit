import sys, argparse, json
try:
    from .core import edit_pdf
    from . import __version__
except (ImportError, ValueError):
    from pdfjin_edit.core import edit_pdf
    from pdfjin_edit import __version__


def main():
    p = argparse.ArgumentParser(prog="pdfjin-edit", description="Apply text edits to a PDF.")
    p.add_argument("input", help="Input PDF file")
    p.add_argument("-t", "--text", required=True, help="Text to add")
    p.add_argument("-x", type=float, default=50, help="X coordinate")
    p.add_argument("-y", type=float, default=50, help="Y coordinate")
    p.add_argument("-o", "--output", required=True, help="Output PDF file")
    p.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    args = p.parse_args()
    try:
        edit_pdf(args.input, [{"text": args.text, "x": args.x, "y": args.y}], output=args.output)
        print(f"Edited PDF saved -> {args.output}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr); sys.exit(1)


if __name__ == "__main__":
    main()
