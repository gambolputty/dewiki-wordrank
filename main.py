import re
from os import listdir
from os.path import join

"""
Reads a list of txt files compiled by "WikiExtractor" and counts word occurrences (case insensitive).
WikiExtractor: https://github.com/attardi/wikiextractor
"""

wikidump_dir = 'G:/Dropbox/Python/_data/WikipediaDe/text'
min_word_len = 2
counts = {}

for d in listdir(wikidump_dir):
    if d.startswith('.'):
        continue

    curr_dir = join(wikidump_dir, d)

    for filename in listdir(curr_dir):
        if filename.startswith('.'):
            continue

        # open file
        file_path = join(curr_dir, filename)
        with open(file_path, 'r', encoding="utf-8") as f:
            lines = f.readlines()
        
        for line in lines:
            if not line:
                continue
            if line.startswith(('<doc', '</doc>')):
                continue

            # clean line
            line = re.sub(r'<!--.+?-->|<ref>.+?</ref>|<nowiki>.+?</nowiki>|<br>', '', line)
                    
            # get word tokens
            words = [w.lower() for w in re.findall(r'\w+', line) if len(w) >= min_word_len and re.match(r'^\d+$', w) is None]
            for word in words:
                counts[word] = counts.get(word, 0) + 1

        # print('Parsed file {}'.format(filename))
    # print('Found {} words'.format(len(counts.keys())))

# create output
output_lines = []
for t in sorted(counts.items(), reverse=True, key=lambda x: x[1]):
    output_lines.append('{}   {}'.format(t[0], t[1]))
output = '\n'.join(output_lines)

# save output
with open('results.txt', mode='w', encoding='utf-8') as f:
    f.write(output)
