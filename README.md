# DrawToLatex

Translate entity relationship diagrams from draw io to LaTeX.

## Limits

It only supports (weak) entity sets, (weak) relationships and attributes. You, yourself, have to change the line to the
identifying relation to a double line. This is done by adding [double] after \draw. If the attribute needs to a key then
use the package `ulem` with `\usepackage[normalem]{ulem}`. The text is then underlined with `\uline{<text>}`. A partial
key can be dash-underlined with `\dashuline{<text>}`.

## Usage

You need to export the diagram from draw io to `.xml`. Then you can use this program with:

```python
$ python3 drawtolatex.py < filename.xml >
```

You can then insert the output from above into a *tikz* environment.

```tex
\begin{tikzpicture}
% <insert here>
\end{tikzpicture}
```

Remember to have *tikz* imported with `\usepackage{tikz}` and

```tex
\usetikzlibrary{er}
```

## Extra commands

If you want then you can use

```tex
\newcommand{\key}[1]{\uline{#1}}
\newcommand{\pkey}[1]{\dashuline{#1}}
```

and then you can use `\key{<text>}` instead of `\uline{<text>}`.

## Test
Feel free to test the program out on the provided `er.xml` with:

```python
$ python3 drawtolatex.py er.xml
```
