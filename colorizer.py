import re
from argparse import ArgumentParser

def parse_arguments():
    parser = ArgumentParser(description='Colorizer of LaTeX equations.\n' \
                            'See accompanying README for instructions of use.')
    parser.add_argument('f', type=str, help='Input file')
    parser.add_argument('--tex', action='store_true')
    return parser.parse_args()

def parse_input_file(f):
    section = None
    colors = {}
    mappings = {}
    equation = []
    for lineno, line in enumerate(f):
        if line.startswith('#'):
            continue
        elif line.strip() == '':
            continue
        elif line.startswith('>'):
            section = get_section(line)
        elif section == 'colors':
            colors = parse_color(line, colors)
        elif section == 'mappings':
            mappings = parse_mapping(line, mappings)
        elif section == 'equation':
            equation = parse_equation(line, equation)
        else:
            msg = f'Badly formatted input file in line {lineno}:\n{line}'
            raise ValueError(msg)
    equation = '\n'.join(equation)
    result = colorize_equation(colors, mappings, equation)
    return result

def get_section(line):
    elements = line[1:].split()
    meaningful = [el for el in elements if el[0] != '#']
    section = meaningful[0].lower()
    if section not in ['colors', 'mappings', 'equation']:
        raise ValueError(f'No section named {section} allowed.')
    return section

def parse_color(line, colors):
    elements = line.split()
    col_name = elements[0]
    try:
        rgb = re.findall('\d+', elements[1])
        rgb = [int(i) for i in rgb]
    except:
        raise ValueError(f'Not a valid RGB string: {elements[1]}')
    colors[col_name] = rgb
    return colors

def parse_mapping(line, mappings):
    elements = line.split()
    symbol = elements[0]
    name = elements[1]
    color = elements[2]
    mappings[symbol] = (name, color)
    return mappings

def parse_equation(line, equation):
    equation.append(line)
    return equation

def colorize_equation(colors, mappings, equation):
    color_definitions = define_colors(colors)
    mapping_definitions = define_mappings(mappings)
    new_elements = []
    eq_elements = equation.split()
    for el in eq_elements:
        if el in mappings.keys():
            name = mappings[el][0]
            col = mappings[el][1]
            s = f'\\{name}{{}}{el}\\plain{{}}'
            new_elements.append(s)
        else:
            new_elements.append(el)
    colorized = ''.join(new_elements)
    final = {'colors': color_definitions,
             'mappings': mapping_definitions,
             'content': colorized}
    return final

def define_colors(colors):
    s = ''
    for col, rgb in colors.items():
        s += f'\\definecolor{{{col}}}{{RGB}}{{{rgb[0]},{rgb[1]},{rgb[2]}}}'
        s += '\n'
    return s

def define_mappings(mappings):
    s = ''
    for symbol, stats in mappings.items():
        name = stats[0]
        col = stats[1]
        s += f'\\newcommand{{\\{name}}}{{\\color{{{col}}}}}'
        s += '\n'
    s += '\\newcommand{\\plain}{\\color{black}}\n'
    return s

def create_full_tex(equation):
    doc = r"""\documentclass[preview]{standalone}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{xcolor}

\begin{document}
\begin{center}
"""
    doc += equation['colors'] + '\n'
    doc += equation['mappings'] + '\n'
    doc += r'\begin{equation*}' + '\n'
    doc += equation['content']
    doc += r"""
\end{equation*}
\end{center}
\end{document}"""
    return doc

def create_string(equation):
    s = ''
    s += equation['colors'] + '\n'
    s += equation['mappings'] + '\n'
    s += r'\begin{equation*}' + '\n'
    s += equation['content'] + '\n'
    s += r'\end{equation*}' + '\n'
    return s

if __name__ == '__main__':
    args = parse_arguments()
    input_file = args.f
    generate_tex = args.tex
    with open(input_file, 'r') as infile:
        result = parse_input_file(infile)
    if generate_tex:
        final_file = create_full_tex(result)
        print(final_file)
    else:
        final_string = create_string(result)
        print(final_string)
