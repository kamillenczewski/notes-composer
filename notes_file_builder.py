from notes_composer import NotesComposer
from os import listdir
from os.path import join

def readFile(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()

def removeFileExtension(path: str):
    dotIndex = path.find('.')

    if dotIndex == -1:
        return path
    
    return path[:dotIndex]

class NotesFileBuilder:
    @classmethod
    def readNote(cls, text):
        lines = text.strip().split('\n')

        title = lines[0]
        text = '\n'.join(lines[1:-1])
        date = lines[-1]

        return title, text, date

    @classmethod
    def fromNotesFolder(cls, inputFolder, outputPath):
        outputPath = removeFileExtension(outputPath)

        composer = NotesComposer()

        names = listdir(inputFolder)
        names = sorted(names, key=lambda name: int(name[:name.index('.')]))

        for fileName in names:
            filePath = join(inputFolder, fileName)
            text = readFile(filePath)
            note = cls.readNote(text)
            composer.addNote(*note)
        
        composer.build(outputPath)

    @classmethod
    def fromFileWithSplitTags(cls, inputPath, outputPath, tag='__note__'):
        outputPath = removeFileExtension(outputPath)

        composer = NotesComposer()

        texts = readFile(inputPath).strip().split(tag)

        for text in texts:
            note = cls.readNote(text)
            composer.addNote(*note)
        
        composer.build(outputPath)