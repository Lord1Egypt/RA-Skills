# Endpoints

## SwissTargetPrediction

- Base: `https://www.swisstargetprediction.ch/`
- Submit: `POST /predict.php`
- Result: `GET /result.php?job=<id>&organism=<organism>`
- Organism values: `Homo_sapiens`, `Mus_musculus`, `Rattus_norvegicus`, `Bos_taurus`, `Sus_scrofa`
- Form fields: `smiles`, `organism`, `ioi=2`
- Notes: no public JSON API, response is job-based and must be polled

## ADMETlab 3.0

- Base: `https://admetlab3.scbdd.com/`
- OpenAPI: `https://admetlab3.scbdd.com/api/openapi.json`
- Single SMILES: `POST /api/single/admet`
- JSON body: `{"SMILES":"...","feature":true|false}`
- Optional body fields: `uncertain`
- Notes: this endpoint is stable enough for scripted use

## PubChem PUG REST

- Base: `https://pubchem.ncbi.nlm.nih.gov/rest/pug`
- Exact CID lookup: `GET /compound/smiles/<SMILES>/cids/JSON`
- Properties: `GET /compound/cid/<CID>/property/MolecularWeight,XLogP,TPSA,HBondDonorCount,HBondAcceptorCount,RotatableBondCount,Complexity,IUPACName,CanonicalSMILES,IsomericSMILES/JSON`
- Synonyms: `GET /compound/cid/<CID>/synonyms/JSON`
- Notes: URL-encode the SMILES; exact lookup can return multiple CIDs

## ChEMBL Data Web Services

- Base: `https://www.ebi.ac.uk/chembl/api/data`
- Similarity search: `GET /similarity/<SMILES>/<cutoff>.json`
- Molecule details: `GET /molecule/<CHEMBL_ID>.json`
- Mechanism lookup: `GET /mechanism.json?molecule_chembl_id=<CHEMBL_ID>`
- Target lookup: `GET /target/<TARGET_CHEMBL_ID>.json`
- Notes: use 90, 80, then 70 similarity cutoffs; fallback if a higher cutoff returns no hits

## PK-Smart Single SMILES

- Base: `https://pk-predictor.serve.scilifelab.se/PKSmart_Single_SMILES`
- Current status: no stable public API confirmed
- Use browser or manual interaction unless a reliable backend endpoint is discovered
