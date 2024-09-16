import os
import argparse
from fontTools.ttLib import TTFont
from fontTools.pens.transformPen import TransformPen

def make_font_narrower(input_folder, output_folder, scale_factor_width=0.75, scale_factor_height=0.85):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".ttf") or filename.endswith(".otf"):  # Process only font files
            font_path = os.path.join(input_folder, filename)
            font = TTFont(font_path)

            # Process glyph outlines in 'glyf' table (for TrueType fonts)
            if 'glyf' in font:
                glyf_table = font['glyf']
                for glyph_name in glyf_table.keys():
                    glyph = glyf_table[glyph_name]
                    if glyph.isComposite():
                        continue  # Skip composite glyphs
                    if glyph.numberOfContours > 0:
                        # Apply both horizontal and vertical scaling
                        pen = TransformPen(glyph, (scale_factor_width, 0, 0, scale_factor_height, 0, 0))  # Narrow horizontally and reduce height
                        glyph.draw(pen)

            # Leave advance width and left side bearing untouched to keep the original spacing
            # Prepare the output file path with "narrow" added to the name
            output_filename = filename.replace(".ttf", "-narrow.ttf").replace(".otf", "-narrow.otf")
            output_path = os.path.join(output_folder, output_filename)

            # Save the modified font to the output folder
            font.save(output_path)
            print(f"Processed: {filename} -> {output_filename}")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Narrow the glyphs in font files.")
    parser.add_argument("input_folder", help="Folder containing the original font files")
    parser.add_argument("output_folder", help="Folder where you want to save the modified fonts")
    parser.add_argument("--scale_factor_width", type=float, default=0.75, help="Scaling factor to narrow the font glyphs horizontally (default: 0.75)")
    parser.add_argument("--scale_factor_height", type=float, default=0.85, help="Scaling factor to reduce the height of the font glyphs (default: 0.85)")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Call the function with the provided arguments
    make_font_narrower(args.input_folder, args.output_folder, args.scale_factor_width, args.scale_factor_height)
