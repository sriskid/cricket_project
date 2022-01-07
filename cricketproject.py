import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

base_url = 'https://stats.espncricinfo.com'

def get_test_century_list():
    t = requests.get('https://stats.espncricinfo.com/ci/engine/player/35320.html?class=1;orderby=batted_score;template=results;type=batting;view=innings')
    t_html = t.text
    return t_html

def get_odi_century_list():
    o = requests.get('https://stats.espncricinfo.com/ci/engine/player/35320.html?class=2;orderby=batted_score;template=results;type=batting;view=innings')
    o_html = o.text
    return o_html

def odi_matches_list(html):
    odi_matches = []
    soup = BeautifulSoup(html, features='html.parser')
    odi = soup.find_all('tr')
    for match in odi[7:56]:
        col = match.find_all('td')
        if col:
            for link in col[13].find_all('a', href=True):
                link_text = link['href']
                link_text = urljoin(base_url, link_text)
            odi_match_data = {
                'runs': col[0].text,
                'minutes': col[1].text,
                'balls faced': col[2].text,
                '4s': col[3].text,
                '6s': col[4].text,
                'strike rate': col[5].text,
                'batting position': col[6].text,
                'opponent': col[10].text,
                'place': col[11].text,
                'date': col[12].text,
                'match id': col[13].text,
                'link': link_text
            }
            odi_matches.append(odi_match_data)
    return odi_matches

def test_matches_list(html):
    matches = []
    soup = BeautifulSoup(html, features='html.parser')
    test_matches = soup.find_all('tr')
    for match in test_matches[7:58]:
        col = match.find_all('td')
        if col:
            for link in col[13].find_all('a', href=True):
                link_text = link['href']
                link_text = urljoin(base_url, link_text)

            match_data = {
                'runs': col[0].text,
                'minutes': col[1].text,
                'balls faced': col[2].text,
                '4s': col[3].text,
                '6s': col[4].text,
                'strike rate': col[5].text,
                'batting position': col[6].text,
                'opponent': col[10].text,
                'place': col[11].text,
                'date': col[12].text,
                'match id': col[13].text,
                'link': link_text
            }
            matches.append(match_data)
    return matches

def combined_matches(t_list, o_list):
    combined_list = t_list + o_list
    return combined_list

def date_sort(row):
    return datetime.strptime(row['date'], '%d %b %Y')
   
def sorted_dates(combined_list):
    sorted_combined_list = sorted(combined_list, key=date_sort)
    return sorted_combined_list

def open_scorecard(match_list,index):
    s = requests.get(match_list[index]['link'])
    s_html = s.text
    return s_html

def parse_scorecard(s_html):
    batting = []
    bowling = []
    
    soup = BeautifulSoup(s_html, features='html.parser')
    scorecard = soup.find_all('table')
    for player in scorecard:
        body = player.find_all('tbody')
        head = player.find('thead')
        for players in body:
            rows = players.find_all('tr')
            if head and 'BATSMEN' in head.text:
                rows = rows[:-1]
                new_list = []
                if rows:
                    for row in rows: 
                        cols = row.find_all('td')

                        if cols:
                            
                            if 'border-0' in cols[0].get('class',''):
                                continue
                            players_performance = {
                                        'name': cols[0].text,
                                        'dismissal': cols[1].text,
                                        'runs': cols[2].text,
                                        'balls faced': cols[3].text,
                                        'minutes': cols[4].text,
                                        '4s': cols[5].text,
                                        '6s': cols[6].text,
                                        'strike rate': cols[7].text
                                    }
                                
                            new_list.append(players_performance)
                            
                batting.append(new_list) 
            elif head and 'BOWLING' in head.text:
                new_list = []
                if rows:
                    for row in rows: 
                        cols = row.find_all('td')

                        if cols:
                            
                            if 'border-0' in cols[0].get('class',''):
                                continue
                            players_performance = {
                                        'name': cols[0].text,
                                        'overs bowled': cols[1].text,
                                        'maidens': cols[2].text,
                                        'runs conceded': cols[3].text,
                                        'wickets': cols[4].text,
                                        'economy': cols[5].text,
                                        'wide balls': cols[9].text,
                                        'no balls': cols[10].text
                                    }
                                
                            new_list.append(players_performance)
                            
                bowling.append(new_list)       
    return batting, bowling

def print_matches(match_data):
    print("SACHIN TENDULKAR CENTURIES".center(165))
    print('Century Number'.center(20),'Runs'.center(10), 'Minutes'.center(10), 'Balls Faced'.center(10), 
            '4s'.center(20), '6s'.center(20), 'Strike Rate'.center(20), 'Batting Position'.center(20),
            'Opponent'.center(20), 'Place'.center(20), 'Date'.center(20), 'Match ID'.center(20))
    print()
    for i, match in enumerate(match_data, start=1):
        print(str(i).center(20), match['runs'].center(10), match['minutes'].center(10), match['balls faced'].center(10), 
        match['4s'].center(20), match['6s'].center(20), match['strike rate'].center(20),
        match['batting position'].center(20),match['opponent'].center(20),match['place'].center(20),
        match['date'].center(20), match['match id'].center(20))
    
def print_scorecard(batting,bowling):
    print('SCORECARD'.center(165))
    for bat,bowl in zip(batting,bowling):
        print('BATSMEN')
        print()
        print('Name'.center(20), 'Dismissal'.center(40), 'Runs'.center(20), 
        'Balls Faced'.center(20), 'Minutes'.center(20), '4s'.center(20), '6s'.center(20), 'Strike Rate'.center(20))
        print()
        for player in bat:
            print(player['name'].center(20), player['dismissal'].center(40), player['runs'].center(20), 
            player['balls faced'].center(20), player['minutes'].center(20), player['4s'].center(20),
            player['6s'].center(20), player['strike rate'].center(20))
        print()
        print('BOWLING')
        print()
        print('Name'.center(20), 'Overs'.center(30), 'Maidens'.center(20), 
        'Runs'.center(20), 'Wickets'.center(20), 'Economy'.center(20), 'Wides'.center(20), 'No Balls'.center(20))
        for bowler in bowl:
            print(bowler['name'].center(20), bowler['overs bowled'].center(30), bowler['maidens'].center(20),
            bowler['runs conceded'].center(20), bowler['wickets'].center(20), bowler['economy'].center(20), bowler['wide balls'].center(20),
            bowler['no balls'].center(20))
        print()

if __name__ == '__main__':
    o_html = get_odi_century_list()
    t_html = get_test_century_list()
    
    odi_matches = odi_matches_list(o_html)
    test_matches = test_matches_list(t_html)
    combined_list = combined_matches(test_matches, odi_matches)

    print('A CENTURY OF CENTURIES!'.center(165))
    print()    
    while True:
        which_table = input('What would you like to see?  1. ODI Centuries    2. Test Centuries    3.Total Centuries ')
        if which_table == '1':
            sorted_list = sorted_dates(odi_matches)
            print_matches(sorted_dates(odi_matches))
            
        elif which_table == '2':
            sorted_list = sorted_dates(test_matches)
            print_matches(sorted_dates(test_matches))
            
        elif which_table == '3':
            sorted_list = sorted_dates(combined_list)
            print_matches(sorted_dates(combined_list))
            
        else:
            print('Cannot do that!')
        
        match_number = int(input('Which century number match would you like to see?  '))
        match_number = match_number - 1
        s_html = open_scorecard(sorted_list,(match_number))
        batting, bowling = parse_scorecard(s_html)
        print_scorecard(batting, bowling)

