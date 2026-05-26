import pandas as pd
import json

def extract_quests(df: pd.DataFrame, skills: list[str], player_stats: dict[str, int], quests_ready: list[str]):
    quest_data = []

    for row_idx in range(3, 181):  # Excel rows 6 to 181
        row = df.iloc[row_idx]
        quest_name = row.iloc[0]  # Assuming quest name is in column A / index 0
        quest_avail = row.iloc[1]
        quest_done = row.iloc[2]
        preReq = row.iloc[3]
        haveStats = row.iloc[4]
        print(f"{quest_name}, {quest_avail}, {quest_done}, {preReq}, {haveStats}")
        unmet_reqs = []

        if not haveStats:
            for i, skill in enumerate(skills):
                cell = row.iloc[5 + i]  # Skill columns start at index 5 (F)
                if pd.isna(cell):
                    continue
                required_level = int(cell)
                current_level = player_stats.get(skill, 0)
                if current_level < required_level:
                    unmet_reqs.append({
                        "skill": skill,
                        "required": required_level,
                        "current": current_level
                    })

        if unmet_reqs:
            quest_data.append({
                "quest": quest_name,
                "available":quest_avail,
                "done":quest_done,
                "preReq":preReq,
                "requirements": unmet_reqs
            })
        else:
            quest_data.append({
                "quest": quest_name,
                "available":quest_avail,
                "done":quest_done,
                "preReq":preReq,
                "requirements": [{"skill":"","required": 0, "current": 0}]
            })
            quests_ready.append(quest_name)

    return quest_data

def total_levels_needed(requirements):
    return sum(req["required"] - req["current"] for req in requirements)

def main():  
    quests_ready = []
    df = pd.read_excel("quest_guide2.xlsx", sheet_name="Normal Runescape Quest Guide")
    OUTPUT_JSON = "quests.json"
    skill_columns = range(5, 28)  # F to AB (assuming 23 skills)
    skills = df.iloc[2, skill_columns].tolist()
    player_levels = df.iloc[0, skill_columns].tolist()
    player_stats = {skill: int(level) for skill, level in zip(skills, player_levels) if not pd.isna(level)}
    quest_list = extract_quests(df, skills, player_stats, quests_ready)
    quest_list.sort(key=lambda q: total_levels_needed(q["requirements"]))
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(quest_list, f, indent=4)

    print(f"✅ Wrote {len(quest_list)} quests with to '{OUTPUT_JSON}'")


if __name__ == "__main__":
    main()
