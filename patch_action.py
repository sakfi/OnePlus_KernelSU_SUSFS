import sys
import re

# Read ASCII art
with open('.github/ascii-new1.txt', 'r', encoding='utf-8') as f:
    lines = f.read().splitlines()

# Strip completely empty or whitespace-only lines from top and bottom
while lines and not lines[0].strip():
    lines.pop(0)
while lines and not lines[-1].strip():
    lines.pop()

# Find the minimum indentation of any non-empty line
min_indent = float('inf')
for line in lines:
    if line.strip():
        indent = len(line) - len(line.lstrip(' '))
        if indent < min_indent:
            min_indent = indent

if min_indent == float('inf'):
    min_indent = 0

# Trim that much indent from every line
trimmed_lines = []
for line in lines:
    if not line.strip():
        trimmed_lines.append('')
    else:
        # Prevent index out of bounds if there's a weird line
        if len(line) >= min_indent and line[:min_indent].isspace():
            trimmed_lines.append(line[min_indent:].rstrip())
        else:
            trimmed_lines.append(line.lstrip().rstrip())

# format as ui_print commands
output_lines = []
for line in trimmed_lines:
    safe_line = line.replace('\\', '\\\\').replace('"', '\\"')
    output_lines.append(f'        ui_print "{safe_line}";')

# Read action.yml
with open('.github/actions/action.yml', 'r', encoding='utf-8') as f:
    action_content = f.read()

# Build bash patcher that runs during GitHub Action
workflow_patch = """        AK3="AnyKernel3/anykernel.sh"
        
        sed -i 's/WildKernels Telegram Channel:/SakFi Kernel Releases:/g' "$AK3"
        sed -i 's|https://t.me/WildKernels|https://github.com/sakfi/OP_KSUN_FS|g' "$AK3"
        sed -i 's/WildKernels Website://g' "$AK3"
        sed -i 's|https://wildkernels.dev||g' "$AK3"
        sed -i 's/Wild_KSU GitHub Repository://g' "$AK3"
        sed -i 's|https://github.com/WildKernels/Wild_KSU||g' "$AK3"
        sed -i 's/KernelSU-Next fork focused on customization and root-hiding features!/OnePlus kernels tailored with KernelSU Next and SUSFS./g' "$AK3"
        sed -i 's/GKI_KernelSU_SUSFS GitHub Repository://g' "$AK3"
        sed -i 's|https://github.com/WildKernels/GKI_KernelSU_SUSFS||g' "$AK3"
        sed -i 's/GKI kernels with KernelSU and SUSFS.//g' "$AK3"
        sed -i 's/OnePlus_KernelSU_SUSFS GitHub Repository://g' "$AK3"
        sed -i 's|https://github.com/WildKernels/OnePlus_KernelSU_SUSFS||g' "$AK3"
        sed -i 's/OnePlus kernels with KernelSU and SUSFS.//g' "$AK3"
        sed -i 's/Wild Kernels by TheWildJames aka Morgan Weedman/SakFi OP Kernels by sakfi/g' "$AK3"
        sed -i '/ui_print "AnyKernel3 by osm0sis @ xda-developers";/a\        ui_print "Wild Kernels by TheWildJames";' "$AK3"
        sed -i '/ui_print "Wild Kernels by TheWildJames";/a\        ui_print "\& fatalcoder524";' "$AK3"
        sed -i 's/Wild Kernels Supported/SakFi Kernels Supported/g' "$AK3"
        
        cat << 'ASCIIEOF' > ascii_art.txt
%s
        ASCIIEOF
        
        sed -i -e '/ui_print "Done!";/r ascii_art.txt' -e '/ui_print "Done!";/d' "$AK3"
        echo 'ui_print "Done! Good Luck with your new Kernel!!";' >> "$AK3"
        
        python3 -c "import re; f=open('$AK3', 'r'); c=f.read(); f.close(); c=re.sub(r'(ui_print \\"\\";\\\\s*){2,}', 'ui_print \\"\\";\\\\n', c); f=open('$AK3', 'w'); f.write(c)"
        rm ascii_art.txt
"""

# Escape correctly for YAML and python string
formatted_ascii = '\n'.join(output_lines)
patch_str = workflow_patch % formatted_ascii

start_idx = action_content.find('# --- Patch AnyKernel3 flashing output for SakFi ---')
end_idx = action_content.find('# --------------------------------------------------', start_idx)

if start_idx != -1 and end_idx != -1:
    new_content = action_content[:start_idx] + '# --- Patch AnyKernel3 flashing output for SakFi ---\n        echo "Patching AnyKernel3 flashing output..."\n' + patch_str + '        # --------------------------------------------------' + action_content[end_idx+52:]
    with open('.github/actions/action.yml', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully patched action.yml content.")
else:
    print("ERROR: Could not find patch block in action.yml. Make sure it exists.")

