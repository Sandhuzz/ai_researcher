# Step1: Import deps
from langchain_core.tools import tool
from datetime import datetime
from pathlib import Path
import subprocess

# Full absolute path to your tectonic.exe
TECTONIC_PATH = r"C:\Users\Asus\Downloads\tectonic-0.15.0-x86_64-pc-windows-msvc\tectonic.exe"

@tool
def render_latex_pdf(latex_content: str) -> str:
    """Render a LaTeX document to PDF using full path to tectonic.exe."""

    # Check if tectonic.exe exists
    if not Path(TECTONIC_PATH).exists():
        raise RuntimeError(
            f"Tectonic was not found at: {TECTONIC_PATH}\n"
            "Update TECTONIC_PATH in write_pdf.py."
        )

    try:
        # Create output directory
        output_dir = Path("output").absolute()
        output_dir.mkdir(exist_ok=True)

        # Filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tex_filename = f"paper_{timestamp}.tex"
        pdf_filename = f"paper_{timestamp}.pdf"

        # Write LaTeX file
        tex_path = output_dir / tex_filename
        tex_path.write_text(latex_content)

        # Run tectonic using absolute path
        result = subprocess.run(
            [
                TECTONIC_PATH,
                tex_filename,
                "--outdir",
                str(output_dir)
            ],
            cwd=output_dir,
            capture_output=True,
            text=True,
        )

        # Check for PDF
        pdf_path = output_dir / pdf_filename
        if not pdf_path.exists():
            print("=== Tectonic output ===")
            print(result.stdout)
            print("=== Tectonic errors ===")
            print(result.stderr)
            raise RuntimeError("PDF was NOT generated. Check LaTeX output.")

        print(f"PDF generated at: {pdf_path}")
        return str(pdf_path)

    except Exception as e:
        print(f"LaTeX rendering error: {e}")
        raise
