#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <random>
#include <ctime>
#include "json.hpp"
#include <set>
using std::string;
using std::vector;
using std::fstream;
using std::cout;
using std::endl;
using std::set;

using json = nlohmann::json;

struct SkillReq {
    string skill;
    int required;
    int current;
};

struct Quest
{
    string name;
    bool available;
    char done;
    bool preReq;
    vector<SkillReq> requirements;
};


vector<Quest> load_quests(const string& filename)
{
    fstream file(filename);
    json j;
    file >> j;
    vector<Quest> quests;
    for(const auto& q : j)
    {
        Quest quest;
        quest.name = q["quest"];
        quest.available = q["available"];
        quest.done = q["done"].get<string>()[0];
        quest.preReq = q["preReq"];
        for(const auto& r : q["requirements"])
        {
            quest.requirements.push_back({
            r["skill"], 
            r["required"],
            r["current"]});
        }
        quests.push_back(quest);
        
        
    }
    return quests;
};

string random_task(const vector<Quest>& quests, std::mt19937 rng)
{
    if (quests.empty()) {
        std::cout << "All quests are done!!" << std::endl;
        return "";
    }

    std::uniform_int_distribution<> quest_dist(0, quests.size() - 1);

    const Quest& q = quests[quest_dist(rng)];

    std::uniform_int_distribution<> skill_dist(0, q.requirements.size() - 1);
    const SkillReq& req = q.requirements[skill_dist(rng)];

    std::stringstream ss;
    if (q.done == 'N' && q.preReq)
    {
        if(q.available && req.skill == "")
        {
            ss << "Do the quest \"" << q.name << "\" since you have all the requirements already!";
        }
        if(req.skill != "")
        {
            ss << "Train " << req.skill << " from " << req.current<< " to " << (req.current + 1) << " to progress toward \"" << q.name << "\"!";
        }

    }
    return ss.str();
};

int main()
{
    vector<Quest> allQuests = load_quests("quests.json");
    

    const int num_tasks = 5;
    set<string> quests;
    while(quests.size() != num_tasks) {
        std::random_device rd;
        std::mt19937 rng(rd());
        string result = random_task(allQuests, rng);
        if(result != "")
        {
            quests.insert(result);
        }
    }
    for(auto& s : quests)
    {
        cout << s << endl;
    }
    return 0;
}
