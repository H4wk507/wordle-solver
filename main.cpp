#include <iostream>
#include <fstream>
#include <json/json.h>
#include <unordered_map>
#include <string>
#include <algorithm>

using namespace std;

std::vector<char> itemgetter(const string &word, const std::vector<int> &indices) {
    std::vector<char> out;
    for (int idx : indices)
        out.push_back(word[idx]);
    return out;
}

int get_num_words(const vector<string> &words, const string &to_guess, const vector<char> &s) {
    int n = 0;
    for (const auto &word : words) {
        int acc = 0;
        for (int i = 0; i < s.size(); i++) {
            vector<int> free_indices;
            for (int j = 0; j < s.size(); j++) {
                if (s[j] != 'g') free_indices.push_back(j);
            }
            vector<char> sliced = itemgetter(word, free_indices);
            if (s[i] == 'g' && word[i] == to_guess[i])
                acc++;
            else if (s[i] == 'y' && find(sliced.begin(), sliced.end(), to_guess[i]) != sliced.end())
                acc++;
            else if (s[i] == 'b' && find(sliced.begin(), sliced.end(), to_guess[i]) == sliced.end())
                acc++;
        }
        if (acc == s.size()) n++;
    }
    return n;
}

int main() {
    ifstream file("wordle_solver/words.json");
    Json::Reader reader;
    Json::Value json_words;
    reader.parse(file, json_words);
    vector<string> words;
    for (const auto &word : json_words) {
        words.push_back(word.toStyledString());
    }
    const int NCOLS = 5;
    const int NWORDS = words.size();
    unordered_map<string, double> freq;
    for (const auto &to_guess : words) {
        for (const auto &word : words) {
            cout << word << '\n';
            vector<char> s('-', NCOLS);
            for (int i = 0; i < NCOLS; i++) {
                vector<int> free_indices;
                for (int j = 0; j < NCOLS; j++) {
                    if (s[j] != 'g') free_indices.push_back(j);
                }
                vector<char> sliced = itemgetter(word, free_indices);
                if (word[i] == to_guess[i]) 
                    s[i] = 'g';
                else if (free_indices.size() > 0 && find(sliced.begin(), sliced.end(), to_guess[i]) != sliced.end())
                    s[i] = 'y';
                else if (free_indices.size() > 0 && find(sliced.begin(), sliced.end(), to_guess[i]) == sliced.end())
                    s[i] = 'b';
            }
            int n = get_num_words(words, to_guess, s);
            freq[word] += n / NWORDS;
        }
    }
}
