import bibtexparser
from pprint import pprint

# +++++++++++++
# CONFIG
# +++++++++++++

BIBFILE = 'bibliography.bib'
OUTFILE = 'syllabus.md'

# Open and parse the bib file
with open(BIBFILE) as bibfile:
    bibliography = bibfile.read()

bib_database = bibtexparser.loads(bibliography)

# Sort into categories 
items = {}
for entry in bib_database.entries:
    
    try:
        cat = entry['category']
    except KeyError:
        cat = 'no_category'
    # Make category if doesn't exist
    if cat not in items.keys():
        items[cat] = []

    # Append entry in relevant category
    items[cat].append(entry)

def writeline(line):
    line = line + '\n\n'
    outfile.write(line)

# Write markdown
with open(OUTFILE, 'w+') as outfile:
    
    # Insert title and initial comments
    writeline('# Text Analysis Community Syllabus')
    writeline('This is an automatically generated document please do not edit this document. If you want to add references insert the information into [`bibliography.bib`](bibliography.bib). See the [readme file](README.md) for details')

    # Write table of contents
    writeline('## Contents')
    for cat in items.keys():
        line = '[{}]({})'.format(cat, cat)   
        writeline(line)

    for cat in items.keys():
        
        line = '## <a name="{}"></a> {}'.format(cat, cat)
        writeline(line)
        
        for entry in items[cat]:
            if entry['ENTRYTYPE'] == 'book':
                line = "{} ({}). *{}*.".format(entry['author'], entry['year'],
                                            entry['title'])
            else:
                try:
                    journal = entry['journal']
                except KeyError:
                    journal = entry['booktitle']
                line = "{} ({}). *{}*. {}.".format(entry['author'], 
                                                  entry['year'],
                                                  entry['title'],
                                                  journal)
            if 'link' in entry.keys():
                line = line + ' [Link]({})'.format(entry['link'])
            writeline(line) 
