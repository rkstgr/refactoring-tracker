from pathlib import Path
from ripgrepy import Ripgrepy
import pandas as pd

REGEX = 'cmd.CommandType = CommandType.StoredProcedure;\n\\s*cmd.CommandText = "sp_(\w+)";'


def main(search_dir: Path):
    import json
    rg = Ripgrepy(REGEX, search_dir.as_posix())
    res = rg.with_filename().multiline().json().run().as_json
    data = json.loads(res)

    result = []
    for match in data:
        file_path = match['data']['path']['text']
        line_number = match['data']['line_number']
        lines = match['data']['lines']['text']
        
        # Extract procedure name from the lines
        for line in lines.split('\n'):
            if "CommandText" in line:
                procedure_name = line.split('"')[1]
                break
        
        result.append({
            "file_path": file_path,
            "line_number": line_number,
            "procedure_name": procedure_name
        })
    
    print("Found {} procedure calls".format(len(result)))

    # save as json
    with open('sql_procedures.json', 'w') as f:
        json.dump(result, f, indent=2)

    # Group by procedure name
    df = pd.read_json('sql_procedures.json')
    grouped_df = df.groupby('procedure_name').agg({
        'file_path': list,
        'line_number': list
    }).reset_index()
    grouped_df = grouped_df.rename(columns={'file_path': 'file_paths', 'line_number': 'line_numbers'})
    grouped_df['occurences'] = grouped_df.apply(lambda row: list(zip(row['file_paths'], row['line_numbers'])), axis=1)
    grouped_data = grouped_df[['procedure_name', 'occurences']].to_dict(orient='records')

    with open('grouped_procedures.json', 'w') as f:
        json.dump(grouped_data, f, indent=2)


if __name__ == "__main__":
    """
    Usage: python main.py <search_dir>
    """
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('search_dir', type=Path)
    args = parser.parse_args()
    main(args.search_dir)