import pandas as pd


def load_rankings() -> dict:
    rankings_df = pd.read_csv('rankings.csv')
    rankings_df = rankings_df.map(lambda cell: ' '.join(cell.split(' ')[1:]).lower())
    rankings_df.columns = [name.lower() for name in rankings_df.columns]
    dicts = {col: {v: i + 1 for i, v in enumerate(rankings_df[col])} for col in rankings_df.columns}
    return dicts


if __name__ == '__main__':
    dicts = load_rankings()