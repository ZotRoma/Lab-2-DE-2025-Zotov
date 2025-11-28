import sys
import re
from deep_translator import GoogleTranslator


def log(message):
    sys.stderr.write(message + "\n")

if len(sys.argv) < 2:
    log("Usage: python translate.py <input_srt>")
    sys.exit(1)

input_file = sys.argv[1]

output_file = sys.argv[2] if len(sys.argv) > 2 else None

translator = GoogleTranslator(source='auto', target='ru')

try:
    log(f"START TRANSLATION")
    
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()
    

    blocks = re.split(r'\n\s*\n', content.strip())
    log(f"Blocks found: {len(blocks)}")

    translated_blocks = []
    
    for block in blocks:
        lines = block.split('\n')
        if len(lines) >= 3:
            original_text = " ".join(lines[2:])
            try:
                translated_text = translator.translate(original_text)

                new_block = f"{lines[0]}\n{lines[1]}\n{translated_text}"
                translated_blocks.append(new_block)
            except Exception as e:
                log(f"Error on block: {e}")
                translated_blocks.append(block)
        else:
            translated_blocks.append(block)

    final_srt = "\n\n".join(translated_blocks)


    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_srt)
        log(f"Saved to {output_file}")


    print(final_srt)

except Exception as e:
    log(f"CRITICAL ERROR: {e}")
    sys.exit(1)