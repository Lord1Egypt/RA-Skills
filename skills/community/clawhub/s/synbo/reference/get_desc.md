## Condition Descriptors

When the user is required to provide Condition Descriptors, they may fulfill this requirement via one of two methods:
1. **Automated Generation:** Instructing you to generate the RDKit descriptors automatically.
2. **File Upload:** Providing pre-calculated tabular files containing the necessary descriptors.

**Automated RDKit Descriptor Generation Protocol:**
If the user requests automated generation, you must strictly adhere to the following workflow:
1. **Prerequisite Check:** You must verify that the Reaction Space data already exists. Automated generation is strictly prohibited if the Reaction Space data is missing.
2. **User Confirmation:** Before executing any calculations, you MUST explicitly ask the user to confirm exactly which reagent categories require descriptor calculation.
3. **Execution:** Once the categories are confirmed, invoke `scripts/get_desc.py` to compute the descriptors for each specified reagent category sequentially. The script should be executed with the following command:
```bash
# --smiles-col and --name-col should be set according to the actual column names in the input CSV files, if they differ from 'SMILES' and 'name'.
python scripts/get_desc.py  --input rxn_space/{reagent_type}.csv --smiles-col 'SMILES' --name-col 'name' 
```

**Attention**: if there are ANY error raised from the descriptor calculation process, you MUST report the error to the user.

**Example output:**
```
✅ Results saved to CSV: descriptors/{reagent_type}_RDKit.csv, data shape is (x, y)
```

**Handling Continuous Variables:**
If the user's submitted conditions include continuous variables (e.g., temperature, time, voltage), do NOT attempt to calculate molecular descriptors for them. Instead, these continuous variables must be formatted and saved in a CSV file using the following strict layout:
```csv
Name,value
[variable_name],[variable_value]
```