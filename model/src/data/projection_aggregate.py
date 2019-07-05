"""Combine aggregated projections into a JSON format usable via the client-side application
"""

import os
import re

import pandas as pd

pd.set_option("display.max_columns", 500)

YEAR = 2019

PROJECTIONS = os.path.join("..", "..", "data", "raw", "projections")
ADP = os.path.join("..", "..", "data", "raw", "adp", f"FFC-{YEAR}.csv")

CBS = os.path.join(PROJECTIONS, f"CBS-Projections-{YEAR}.csv")
ESPN = os.path.join(PROJECTIONS, f"ESPN-Projections-{YEAR}.csv")
NFL = os.path.join(PROJECTIONS, f"NFL-Projections-{YEAR}.csv")

OUTPUT = os.path.join("..", "..", "data", "processed", f"Projections-{YEAR}")

REG = r"(.*?)_([a-zA-Z0-9])"

HEADERS = ["key", "name", "pos", "team", "bye"]

STATS = {
    "pass_tds",
    "pass_yds",
    "pass_ints",
    "rush_tds",
    "rush_yds",
    "receptions",
    "reception_tds",
    "reception_yds",
    "two_pts",
    "fumbles",
    "kick_0_19",
    "kick_20_29",
    "kick_30_39",
    "kick_40_49",
    "kick_50",
    "kick_extra_points",
    "df_points_allowed_per_game",
    "df_sacks",
    "df_safeties",
    "df_fumbles",
    "df_tds",
    "df_ints",
}

COLS = HEADERS + list(STATS)


def aggregate():
    """Read in CBS, ESPN, Fox projections and ADP and outputs a
    forecast.json for the application
    """

    src = ["cbs", "espn", "nfl"]

    df = pd.read_csv(ADP)
    df = df.set_index("key")
    for i, other in enumerate([CBS, ESPN, NFL]):
        other_df = pd.read_csv(other)
        other_df = other_df.set_index("key")
        other_df = other_df.drop(["name", "pos", "team"], axis=1)
        other_df.columns = [h + "_" + src[i] for h in other_df.columns]

        df = df.join(other_df)
    df = df.sort_values("adp_8_ppr")

    for stat in STATS:
        stat_cols = [c for c in df.columns if stat in c]
        df[stat] = df[stat_cols].mean(axis=1)

    # keep only the means
    df = df.reset_index()
    adps = sorted([c for c in df.columns if "adp" in c])
    df = df[COLS + adps]
    df = df.round(1)

    for adp in adps:
        df[adp] = df[adp].fillna(-1).astype(int)

    df.to_csv(OUTPUT + ".csv", index=False)

    df.columns = [re.sub(REG, camel, c, 0) for c in df.columns]

    df.to_json(OUTPUT + ".json", orient="table")


def camel(match):
    return match.group(1) + match.group(2).upper()


if __name__ == "__main__":
    aggregate()