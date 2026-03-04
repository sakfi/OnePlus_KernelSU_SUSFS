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
    output_lines.append(f'ui_print "{safe_line}"')

# Read action.yml
with open('.github/actions/action.yml', 'r', encoding='utf-8') as f:
    action_content = f.read()

# Build python patcher that runs during GitHub Action
workflow_patch = '''
        cat << 'EOF' > patch_anykernel.py
import sys
import re

with open('AnyKernel3/anykernel.sh', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace texts
content = content.replace('WildKernels Telegram Channel:', 'SakFi Kernel Releases:')
content = content.replace('https://t.me/WildKernels', 'https://github.com/sakfi/OP_KSUN_FS')
content = content.replace('WildKernels Website:', '')
content = content.replace('https://wildkernels.dev', '')
content = content.replace('Wild_KSU GitHub Repository:', '')
content = content.replace('https://github.com/WildKernels/Wild_KSU', '')
content = content.replace('KernelSU-Next fork focused on customization and root-hiding features!', 'OnePlus kernels tailored with KernelSU Next and SUSFS.')
content = content.replace('GKI_KernelSU_SUSFS GitHub Repository:', '')
content = content.replace('https://github.com/WildKernels/GKI_KernelSU_SUSFS', '')
content = content.replace('GKI kernels with KernelSU and SUSFS.', '')
content = content.replace('OnePlus_KernelSU_SUSFS GitHub Repository:', '')
content = content.replace('https://github.com/WildKernels/OnePlus_KernelSU_SUSFS', '')
content = content.replace('OnePlus kernels with KernelSU and SUSFS.', '')

content = content.replace('Wild Kernels by TheWildJames aka Morgan Weedman', 'SakFi OP Kernels by sakfi')
content = content.replace('AnyKernel3 by osm0sis @ xda-developers', 'AnyKernel3 by osm0sis @ xda-developers\\\\nui_print "Wild Kernels by TheWildJames"\\\\nui_print "& fatalcoder524"')
content = content.replace('Wild Kernels Supported', 'SakFi Kernels Supported')

# Inject ASCII replacing 'Done!'
ascii_commands = """%s"""

lines = content.split('\\n')
for i, line in enumerate(lines):
    if 'ui_print "Done!";' in line:
        art_lines = [l+";" for l in ascii_commands.splitlines() if l.strip()]
        lines.insert(i, '\\n'.join(art_lines))
        break

content = '\\n'.join(lines)
content = content.replace('ui_print "Done!";', 'ui_print "Done! Good Luck with your new Kernel!!";')

# Remove duplicate empty ui_prints caused by deleted urls
content = re.sub(r'(ui_print "";\\s*){2,}', 'ui_print "";\\n', content)

with open('AnyKernel3/anykernel.sh', 'w', encoding='utf-8') as f:
    f.write(content)
EOF
        python3 patch_anykernel.py
        rm patch_anykernel.py
'''

# Escape correctly for YAML and python string
formatted_ascii = '\\n'.join(output_lines)
patch_str = workflow_patch % formatted_ascii.replace('\\', '\\\\')

start_idx = action_content.find('# --- Patch AnyKernel3 flashing output for SakFi ---')
end_idx = action_content.find('# --------------------------------------------------', start_idx)

if start_idx != -1 and end_idx != -1:
    new_content = action_content[:start_idx] + '# --- Patch AnyKernel3 flashing output for SakFi ---\n        echo "Patching AnyKernel3 flashing output..."\n' + patch_str + '        # --------------------------------------------------' + action_content[end_idx+52:]
    with open('.github/actions/action.yml', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully patched action.yml content.")
else:
    print("ERROR: Could not find patch block in action.yml. Make sure it exists.")
