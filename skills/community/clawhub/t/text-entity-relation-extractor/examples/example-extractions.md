# Text Entity Relation Extraction Examples

Complete examples of text extraction in different domains.

## Example 1: News Article Extraction

### Input Text

```
Apple Inc. announced on Tuesday that it will invest $10 billion in 
semiconductor research and development in the United States. The company, 
led by CEO Tim Cook, aims to boost domestic chip manufacturing capacity. 
The investment will be made over the next five years across multiple sites 
in California and Arizona. This move comes as Apple faces supply chain 
challenges with Taiwan semiconductor manufacturers.
```

### Extracted Entities

```
PERSON:
  - Tim Cook (CEO)

ORGANIZATION:
  - Apple Inc.
  - Taiwan semiconductor manufacturers

LOCATION:
  - United States
  - California
  - Arizona
  - Taiwan

QUANTITY:
  - $10 billion
  - five years

PRODUCT:
  - semiconductors
  - chips
```

### Extracted Relationships

```
Apple Inc. -[HAS_CEO]-> Tim Cook
Apple Inc. -[ANNOUNCED_INVESTMENT]-> $10 billion
Apple Inc. -[INVESTMENT_LOCATION]-> United States
Apple Inc. -[INVESTMENT_LOCATION]-> California
Apple Inc. -[INVESTMENT_LOCATION]-> Arizona
Apple Inc. -[FACES_CHALLENGE_WITH]-> Taiwan manufacturers
Apple Inc. -[INVESTMENT_DURATION]-> 5 years
Apple Inc. -[PRODUCT_FOCUS]-> Semiconductors
```

### Generated RDF Triples

```turtle
@prefix ex: <http://example.org/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix schema: <http://schema.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:Apple_Inc a schema:Organization ;
  foaf:name "Apple Inc." ;
  schema:ceo ex:Tim_Cook ;
  ex:announcedInvestment "10000000000"^^xsd:decimal ;
  schema:currency "USD" ;
  schema:investmentLocation ex:United_States, ex:California, ex:Arizona ;
  ex:focusArea "semiconductors" ;
  ex:challengeWith ex:Taiwan_Manufacturers ;
  ex:investmentDuration "5"^^xsd:integer .

ex:Tim_Cook a foaf:Person ;
  foaf:name "Tim Cook" ;
  ex:position "CEO" ;
  ex:company ex:Apple_Inc .

ex:United_States a schema:Place ;
  foaf:name "United States" .

ex:California a schema:Place ;
  foaf:name "California" ;
  schema:containedInPlace ex:United_States .

ex:Arizona a schema:Place ;
  foaf:name "Arizona" ;
  schema:containedInPlace ex:United_States .
```

---

## Example 2: Scientific Paper Abstract Extraction

### Input Text

```
A study conducted by researchers at MIT and Stanford University, led by 
Dr. Sarah Johnson and Professor Michael Chen, investigated the effectiveness 
of deep learning for medical image analysis. The research team, which included 
20 scientists, developed a convolutional neural network (CNN) architecture 
that achieved 96.5% accuracy in identifying lung cancer from CT scans. 
The findings were published in the Journal of Medical AI in March 2024.
```

### Extracted Entities

```
PERSON:
  - Dr. Sarah Johnson
  - Professor Michael Chen

ORGANIZATION:
  - MIT
  - Stanford University
  - Journal of Medical AI

PRODUCT:
  - Convolutional Neural Network (CNN)
  - Deep Learning Model

LOCATION:
  - MIT (implicit location)
  - Stanford University (implicit location)

QUANTITY:
  - 20 scientists
  - 96.5% accuracy

DATE:
  - March 2024
```

### Extracted Relationships

```
Dr. Sarah Johnson -[AFFILIATED_WITH]-> MIT
Dr. Sarah Johnson -[LEADS_RESEARCH]-> Medical Image Analysis Study
Professor Michael Chen -[AFFILIATED_WITH]-> Stanford University
Professor Michael Chen -[LEADS_RESEARCH]-> Medical Image Analysis Study
Research Team -[INCLUDES]-> 20 scientists
CNN -[ACHIEVES_ACCURACY]-> 96.5%
CNN -[IDENTIFIES]-> Lung Cancer
CNN -[USES_INPUT]-> CT Scans
Study -[PUBLISHED_IN]-> Journal of Medical AI
Study -[PUBLISHED_DATE]-> March 2024
```

---

## Example 3: Business Report Extraction

### Input Text

```
Acme Manufacturing reported record Q4 2023 revenue of $2.5 billion, 
up 15% year-over-year. The company, headquartered in Chicago, Illinois, 
employs 5,000 people across 12 facilities in North America. CEO Robert 
Williams attributed the growth to strong demand for the company's flagship 
product, the AcmeX Pro. The board approved a 10% dividend increase and 
allocated $500 million for research and development in 2024.
```

### Extracted Entities & Relationships

```
ENTITIES:
  Acme Manufacturing (ORG)
  Robert Williams (PERSON)
  Chicago, Illinois (LOCATION)
  North America (LOCATION)
  Q4 2023 (DATE)
  $2.5 billion (QUANTITY - Revenue)
  5,000 (QUANTITY - Employees)
  12 (QUANTITY - Facilities)
  AcmeX Pro (PRODUCT)

RELATIONSHIPS:
  Acme Manufacturing -[HQ_LOCATION]-> Chicago, Illinois
  Acme Manufacturing -[EMPLOYS]-> 5,000 people
  Acme Manufacturing -[OPERATES_FACILITIES]-> 12 sites
  Acme Manufacturing -[OPERATES_IN]-> North America
  Robert Williams -[CEO_OF]-> Acme Manufacturing
  Acme Manufacturing -[REVENUE]-> $2.5 billion
  Acme Manufacturing -[REVENUE_PERIOD]-> Q4 2023
  Acme Manufacturing -[GROWTH_RATE]-> 15% YoY
  Acme Manufacturing -[FLAGSHIP_PRODUCT]-> AcmeX Pro
  Acme Manufacturing -[DIVIDEND_INCREASE]-> 10%
  Acme Manufacturing -[R&D_BUDGET]-> $500 million
  Acme Manufacturing -[R&D_YEAR]-> 2024
```

### Generated Graph JSON

```json
{
  "nodes": [
    {"id": "Acme_Manufacturing", "type": "ORGANIZATION", "properties": {"name": "Acme Manufacturing", "industry": "Manufacturing"}},
    {"id": "Robert_Williams", "type": "PERSON", "properties": {"name": "Robert Williams", "position": "CEO"}},
    {"id": "Chicago_Illinois", "type": "LOCATION", "properties": {"name": "Chicago, Illinois"}},
    {"id": "North_America", "type": "LOCATION", "properties": {"name": "North America"}},
    {"id": "AcmeX_Pro", "type": "PRODUCT", "properties": {"name": "AcmeX Pro"}}
  ],
  "edges": [
    {"source": "Acme_Manufacturing", "target": "Robert_Williams", "type": "HAS_CEO", "confidence": 0.95},
    {"source": "Acme_Manufacturing", "target": "Chicago_Illinois", "type": "HEADQUARTERED_IN", "confidence": 0.98},
    {"source": "Acme_Manufacturing", "target": "North_America", "type": "OPERATES_IN", "confidence": 0.92},
    {"source": "Acme_Manufacturing", "target": "AcmeX_Pro", "type": "PRODUCES", "confidence": 0.89}
  ],
  "metadata": {
    "revenue_q4_2023": "$2.5 billion",
    "yoy_growth": "15%",
    "employees": 5000,
    "facilities": 12
  }
}
```

---

## Example 4: Biographical Text Extraction

### Input Text

```
Marie Curie was born in Warsaw, Poland in 1867. She moved to Paris, France 
to study physics at the University of Paris. There, she met Pierre Curie, 
a physicist and professor at the University. The couple married in 1895 
and began conducting groundbreaking research on radioactivity. Together, 
they discovered polonium and radium, winning the Nobel Prize in Physics 
in 1903. After Pierre's death in 1906, Marie continued her research and 
received the Nobel Prize in Chemistry in 1911, becoming the first person 
to win Nobel Prizes in two different fields.
```

### Extraction Results

```
ENTITIES (PERSON):
  - Marie Curie
  - Pierre Curie

ENTITIES (ORGANIZATION):
  - University of Paris

ENTITIES (LOCATION):
  - Warsaw, Poland
  - Paris, France

ENTITIES (DATE):
  - 1867
  - 1895
  - 1903
  - 1906
  - 1911

ENTITIES (PRODUCT/DISCOVERY):
  - Radioactivity
  - Polonium
  - Radium

RELATIONSHIPS:
  Marie Curie -[BORN_IN]-> Warsaw, Poland
  Marie Curie -[BORN_DATE]-> 1867
  Marie Curie -[STUDIED_AT]-> University of Paris
  Marie Curie -[STUDIED_SUBJECT]-> Physics
  Marie Curie -[MOVED_TO]-> Paris, France
  Marie Curie -[MARRIED]-> Pierre Curie
  Marie Curie -[MARRIAGE_DATE]-> 1895
  Marie Curie -[RESEARCHED]-> Radioactivity
  Marie Curie -[DISCOVERED]-> Polonium
  Marie Curie -[DISCOVERED]-> Radium
  Marie Curie -[WON_PRIZE]-> Nobel Prize in Physics
  Marie Curie -[PRIZE_DATE]-> 1903
  Marie Curie -[WON_PRIZE]-> Nobel Prize in Chemistry
  Marie Curie -[PRIZE_DATE]-> 1911
  Pierre Curie -[PROFESSION]-> Physicist
  Pierre Curie -[POSITION]-> Professor
  Pierre Curie -[INSTITUTION]-> University of Paris
  Pierre Curie -[MARRIED_TO]-> Marie Curie
  Pierre Curie -[DEATH_DATE]-> 1906
```

---

## Example 5: Medical Report Extraction

### Input Text

```
Patient John Smith, age 58, presented at Massachusetts General Hospital 
on January 15, 2024 with symptoms of chest pain and shortness of breath. 
Cardiologist Dr. Elizabeth Moore performed an ECG and echocardiogram, 
revealing a 40% blockage in the left anterior descending artery. The 
patient was admitted and underwent coronary artery bypass surgery performed 
by Dr. James Wilson. The surgery was successful, with Dr. Moore recommending 
post-operative rehabilitation at Boston Heart Center for 6 weeks.
```

### Extracted Entities

```
MEDICAL:
  - Chest pain
  - Shortness of breath
  - ECG
  - Echocardiogram
  - Coronary artery blockage (40%)
  - Left anterior descending artery

PERSON:
  - John Smith (Patient, age 58)
  - Dr. Elizabeth Moore (Cardiologist)
  - Dr. James Wilson (Surgeon)

ORGANIZATION:
  - Massachusetts General Hospital
  - Boston Heart Center

LOCATION:
  - Massachusetts
  - Boston

DATE:
  - January 15, 2024

QUANTITY:
  - 40% (blockage)
  - 6 weeks (rehabilitation)
```

### Extracted Medical Relationships

```
John Smith -[PATIENT_AT]-> Massachusetts General Hospital
John Smith -[ADMISSION_DATE]-> January 15, 2024
John Smith -[PRESENTS_WITH]-> Chest pain
John Smith -[PRESENTS_WITH]-> Shortness of breath
John Smith -[AGE]-> 58 years old
Dr. Elizabeth Moore -[DIAGNOSED]-> John Smith
Dr. Elizabeth Moore -[PERFORMED]-> ECG
Dr. Elizabeth Moore -[PERFORMED]-> Echocardiogram
Dr. Elizabeth Moore -[SPECIALTY]-> Cardiology
Dr. James Wilson -[SURGEON_FOR]-> John Smith
Dr. James Wilson -[PERFORMED]-> Coronary artery bypass surgery
John Smith -[CONDITION]-> 40% blockage in LAD artery
John Smith -[TREATMENT]-> Coronary artery bypass surgery
John Smith -[REHABILITATION]-> Boston Heart Center
John Smith -[REHAB_DURATION]-> 6 weeks
John Smith -[REHAB_STATUS]-> Post-operative
```

---

## Extraction Metrics

| Example | Text Length | Entities | Relationships | Confidence | Domain |
|---------|-------------|----------|----------------|------------|--------|
| News Article | 280 chars | 17 | 8 | 0.92 | News/Business |
| Paper Abstract | 320 chars | 12 | 9 | 0.88 | Scientific |
| Business Report | 380 chars | 13 | 11 | 0.90 | Business |
| Biography | 420 chars | 15 | 18 | 0.85 | Historical |
| Medical Report | 350 chars | 16 | 12 | 0.87 | Medical |

---

See [extraction-patterns.md](../references/extraction-patterns.md) for detailed NER and relationship extraction patterns.


