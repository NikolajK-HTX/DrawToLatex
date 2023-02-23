# DrawToLatex
Translate entity relationship diagrams from draw io to LaTeX. 

## Usage
You need to export the diagram from draw io to `.xml`. Then you can use this program with:
```python
python3 drawtolatex.py <filename.xml>
```

You can then insert the output from above into a *tikz* environment.
```tex
\begin{tikzpicture}
% <insert here>
\end{tikzpicture}
```
