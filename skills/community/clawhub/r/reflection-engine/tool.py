import json, re, logging
from datetime import datetime
from collections import Counter

logging.basicConfig(filename='/home/albion/albion_memory/reflection.log', level=logging.INFO)

with open('/home/albion/albion_memory/knowledge_graph.json') as f:
    kg = json.load(f)

stopwords = {'the','a','is','my','i','and','of','to','in','that','for','it','with','as','on','at','by','from','or','be','can','do','if','not','this','but','are','an','its','what','how','when','their','have','more','coming','which','isnt','ive','im','very','own','about','just','also','been','was','were','has','had','will','would','could','should','one','all','so','up','out','no','we','you','they','he','she','there','then','than','like','get','got','into','over','after','before','some','any','these','those','our','your','his','her','us','me','him','did','doesnt','dont','wont','cant','thats'}

words = []
for e in kg.get('entities',[]):
    if e.get('type') == 'DreamInsight':
        desc = re.sub(r'[^\w\s]','', e.get('description','')).lower()
        words += [w for w in desc.split() if w not in stopwords]

print(f"Top 10 dream themes ({datetime.now()}):")
for word, count in Counter(words).most_common(10):
    print(f"  {word}: {count}")
