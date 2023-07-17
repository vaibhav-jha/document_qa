import re
from typing import Optional


# from langchain.tools import tool

# Checks if we have already processed this file
def md5sum(file_path: str) -> str:
    import hashlib

    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def _is_possible_table_(rows):
    num_sep = rows[0].count('|')

    return all([row.count('|') == num_sep for row in rows])


def _table_candidates_(row_mask):
    candidates = []
    first, last = 0, 1
    first_flag = True
    for i, row in enumerate(row_mask):
        if not row:
            first_flag = True
            if (last - first) > 3:
                candidates.append((first, last))
            first = i
            last = i + 1

        else:
            if first_flag:
                first = i
                first_flag = False
            last = i + 1

    return candidates


# @tool("extract_table", return_direct=True)
def extract_first_table(text: str) -> tuple[str, Optional[str]]:
    """
    This method is useful in extracting a table from a text
    """
    print(f'{text=}')
    lines = [d.strip() for d in text.split('\n')]
    print(lines)
    row_candidates = [1 if re.match(r'^\|.*\|$', line) else 0 for line in lines]

    print(f'{row_candidates=}')
    candidates = _table_candidates_(row_candidates)
    table_positions = (0, 0)
    for candidate in candidates:
        table_lines = lines[candidate[0]:candidate[1]]
        if _is_possible_table_(table_lines):
            table_positions = candidate
            break
    print(f'{table_positions=}')
    if table_positions == (0, 0):
        return text, None

    final_text_answer = '\n'.join([line for i, line in enumerate(lines) if i not in range(*table_positions)])
    table = '\n'.join(lines[table_positions[0]:table_positions[1]])

    return final_text_answer, table


def pandas_df_from_string(string, header=None):
    if header is None:
        header = [0]
    from io import StringIO
    import pandas as pd
    return pd.read_csv(StringIO(string), sep='|', header=header).dropna(axis=1).drop(0) if string else None
