from pylatex import Document, NoEscape
from os import remove

class NotesComposer:
    def __init__(self):
        self.margin = '3cm'

        self.font = 'Lexend'

        self.titleFontSize = '15pt'
        self.titleFontWeight = 'Bold'

        self.textFontSize = '11pt'
        self.textFontWeight = 'Normal'

        self.dateFontSize = '11pt'
        self.dateFontWeight = 'Normal'

        self.spacingBetweenLinesInTableOfContents = '2pt'
        self.spacingFactorBetweenLines = '1.3'

        self.tableOfContentsTitle = 'Spis treści'
        self.mainTitle = 'Wiersze'

        self.document = Document(
            documentclass="article",
            fontenc=None,
            inputenc=None,
            lmodern=False,
            geometry_options={
                "margin": self.margin
            }
        )

        self.addToPreamble(NoEscape(r"\usepackage{fontspec}"))
        self.addToPreamble(NoEscape(r"\setmainfont{" + self.font + "}"))
        self.addToPreamble(NoEscape(r'\linespread{' + self.spacingFactorBetweenLines + '}')) 

        self.addToPreamble(NoEscape(r'\setlength{\parindent}{0pt}'))
        
        self.addToPreamble(NoEscape(r'\usepackage{tocloft}'))
        self.addToPreamble(NoEscape(r'\setlength{\cftbeforesecskip}{' + self.spacingBetweenLinesInTableOfContents + '}')) 

        self.addToPreamble(NoEscape(r'\renewcommand{\contentsname}{' + self.tableOfContentsTitle + '}'))

        self.document.append(NoEscape(r'{\centering\fontsize{30pt}{36pt}\selectfont\textbf{' + self.mainTitle + r'}\par}'))

        self.add(NoEscape(r'\tableofcontents'))
        self.add(NoEscape(r'\newpage'))
    
    def add(self, content):
        self.document.append(content)

    def addToPreamble(self, content):
        self.document.preamble.append(content)


    def addNote(self, title, text, date):
        text = text.strip().replace('\n', r'\\')

        self.add(NoEscape(
            # title
            r'{'
            r'\fontsize{16pt}{20pt}\selectfont\section*{' + title + r'}'
            r'\addcontentsline{toc}{section}{' + title + r'}'
            r'\par'

            # text
            r'\fontsize{' + self.textFontSize + r'}{10pt}\selectfont\addfontfeatures{Weight=' + self.textFontWeight + r'} ' +
            text + r'\par'

            # space before date
            r'\vspace{10pt}'

            # date
            r'\fontsize{' + self.textFontSize + r'}{10pt}\selectfont\addfontfeatures{FakeSlant=0.3, Weight=' + self.textFontWeight + r'} ' +
            date + r'\par' 

            r'}'
        ))
    

    def build(self, outputName):
        self.document.generate_pdf(outputName, compiler="lualatex", clean_tex=True)
        self.document.generate_pdf(outputName, compiler="lualatex", clean_tex=True)
        remove(outputName + '.toc')