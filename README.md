Equation Colorizer
==================

This is a simple Python package to generate colorized equations. The user
writes a simple input file in a custom language, then runs

    python colorizer.py input.txt

The output is the colorized equation in LaTeX format, plus necessary
definitions. This can be copied and pasted into any document. If, instead, you
want to generate a minimal working `.tex` file with all the scaffolding in
place, run

    python colorizer.py --tex input.txt

The compilation of the output is left to the user. With a good LaTeX
distribution installed, simple compilation can be achieved by

    python colorizer.py --tex input.txt > pdflatex

For now, the script only runs on Python 3.

Input file
==========

The input is composed of three sections: color definitions, mappings from
symbols to colors, and the equation itself. A section is prefixed by the symbol
`>`, followed by any amount of whitespace, followed by the word `colors`,
`mappings`, or `equations`, in any capitalization. Outside of this context,
whitespace is ignored. You can include comment lines that start with `#`.

**Color definitions:** Colors are defined by a name, followed by whitespace,
followed by RGB values within parentheses and separated by commas. Each line
contains one color.

**Mappings:** Mappings consist of three elements separated by whitespace: LaTeX
symbols, an identifier, and the name of the color the symbol should be colored
as. To have multiple symbols share a color, include them in different lines.
Each line contains one mapping.  The symbol can be a LaTeX string of any length
and complexity, and it doesn't need enclosing `$`s.

**Equation:** The equation itself, written in LaTeX format. This can be an
arbitrary string; the user is responsible for managing the LaTeX document and
making sure all the required packages are included before compiling.
Importantly, any symbols that are to be colorized need to be surrounded by
whitespace (which is ignored by LaTeX anyway). This is to avoid ambiguity; if
the user defines a mapping `M: blue`, then the string `M^2` will not be
colorized, but in the string `M ^2` the M will be properly blue.

Usage should be clear from the example file below:

    # Example input file to colorize the logistic growth equation.

    > colors
    # ColorBrewer 4-class qualitative palette
    red		 (228,26,28)
    blue 	 (55,126,184)
    green 	 (77,175,74)
    purple 	 (152,78,163)

    > Mappings

    N   popSize    blue    # population size
    dN  diffSize   blue    # differential of population size
    dt  diffTime   green   # differential of time
    r   growthRate purple  # growth rate
    K   carrCap    red     # carrying capacity

    > EQUATION

    \frac{ dN }{ dt }
    = r N \cdot \left( 1 - \frac{ N }{ K }\right)

The output is:

    \definecolor{red}{RGB}{228,26,28}
    \definecolor{blue}{RGB}{55,126,184}
    \definecolor{green}{RGB}{77,175,74}
    \definecolor{purple}{RGB}{152,78,163}

    \newcommand{\popSize}{\color{blue}}
    \newcommand{\diffSize}{\color{blue}}
    \newcommand{\diffTime}{\color{green}}
    \newcommand{\growthRate}{\color{purple}}
    \newcommand{\carrCap}{\color{red}}
    \newcommand{\plain}{\color{black}}

    \begin{equation*}
    \frac{\diffSize{}dN\plain{}}{\diffTime{}dt\plain{}}=\growthRate{}r\plain{}\popSize{}N\plain{}\cdot\left(1-\frac{\popSize{}N\plain{}}{\carrCap{}K\plain{}}\right)
    \end{equation*}
