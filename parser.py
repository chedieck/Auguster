import os
import regex as re





def parsefile(f):
    """
    returns the file with the title between 0t0, 0v0 between verses, 0e0 between estrofes and 0f0 at the end of the file
    """
    title, text = f.read().split('\n', 1)
    estrofes = re.split('\n\n+', text)
    estrofes = [e for e in estrofes if e] #remove empty strings
    text = ' 0e0 '.join(estrofes)
    versos = re.split('\n', text)
    versos = [v for v in versos if v] #remove empty strings
    text = ' 0v0 '.join(versos)
    return ' 0t0 ' + title + ' 0t0 ' + text + ' 0f0 '
    

def main():
    files = os.listdir('DB')
    poems = ''
    for strf in files:
        with open(f'DB/{strf}', 'r') as f:
            poem = parsefile(f)
            poems += poem + '\n'
    poems = poems[:-1] #remove last \n
    with open('poems.txt', 'w') as p:
        p.write(poems)



