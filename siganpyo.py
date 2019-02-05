from selenium import webdriver
import sys
import unicodedata
import time

def string_preformat(string, width, align='<', fill=' '):
    count = (width - sum(1 + (unicodedata.east_asian_width(c) in "WF")
                         for c in string))
    return {
        '>': lambda s: fill * count + s,
        '<': lambda s: s + fill * count,
        '^': lambda s: fill * (count / 2)
                       + s
                       + fill * (count / 2 + count % 2)
}[align](string)

def input_information():
    print(
    '''
                _   _       _   _            ____                      _ 
                | \ | |     | | (_)          |  _ \                    | |
                |  \| | ___ | |_ _  ___ ___  | |_) | ___   __ _ _ __ __| |
                | . ` |/ _ \| __| |/ __/ _ \ |  _ < / _ \ / _` | '__/ _` |
                | |\  | (_) | |_| | (_|  __/ | |_) | (_) | (_| | | | (_| |
                |_| \_|\___/ \__|_|\___\___| |____/ \___/ \__,_|_|  \__,_|                                                                                           
    '''
    )
    print('          Which provinces do you live in?  :  (지역 이름 EX) 서울, 경기, 세종, ...)')
    local  = input().strip()

    print('          What is name of your school?  :  (학교 이름 전체 EX) 고운중학교)')
    school = input().strip()

    print('          What grade are you in?   :  (몇 학년인지 EX) 3)')
    grade = input().strip()

    print('          What is your class?   :  (몇 반인지 EX) 11)')
    cla = input().strip()
    return local, school, int(grade), int(cla)

def input_menu():
    print(
    '''
                    1_시간표 알아보기
                    2_급식 알아보기
                    3_학교 정보 변경하기
                    0_종료하기
     
    ''', end="")
    select = input("메뉴를 선택해주세요: ")
    return select

def siganpyo(school, grade, cla):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome('../chromedriver.exe', options=options)

    driver.get('http://comci.kr:4081/st')
    driver.implicitly_wait(3)

    driver.find_element_by_name('sc2').send_keys(school)
    driver.find_element_by_xpath('//*[@id="학교찾기"]/table[1]/tbody/tr[2]/td[2]/input[2]').click()

    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="학교명단검색"]/tbody/tr[2]/td[2]/a').click()

    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="ba"]').click()

    findClass = True
    while (True):
        x = driver.find_element_by_xpath('//*[@id="hour"]/table/tbody/tr[1]/td[2]').text.split()
        if int(x[1]) == grade and int(x[3]) == cla:
            findClass = True
            break
        elif int(x[1]) == 1 and int(x[3]) == 1:
            if findClass:
                findClass = False
            else:
                print("%s에 %d학년 %d반은 없습니다." % (school, int(grade), int(cla)))
                driver.quit()
                main()
                return False
        driver.find_element_by_xpath('//*[@id="hour"]/table/tbody/tr[1]/td[1]/input').click()

    if (findClass):
        print("-----------------------------------------------")
        print("|    교시  |  월  |  화  |  수  |  목  |  금  |")
        print("-----------------------------------------------")
        for i in range(3,10):
            teacher_list = []
            classtime = driver.find_element_by_xpath('//*[@id="hour"]/table/tbody/tr[%d]/td[1]'% (i)).text
            print("| %s |" % classtime, end="")

            for j in range(2,7):
                subject = driver.find_element_by_xpath('//*[@id="hour"]/table/tbody/tr[%d]/td[%d]'% (i, j)).text.split()

                if(len(subject) > 0):
                    print("%s" % string_preformat(subject[0], 6), end="|")
                    teacher_list.append(subject[1])
                else:
                    print("      ", end="|")
                    teacher_list.append("      ")
            print("")

            print("|          |", end="")
            for teacher_name in teacher_list:
                print("%s" % string_preformat(teacher_name, 6), end="|")
            print("")
            print("-----------------------------------------------")

    driver.quit()
    return True

def geupsik(local, school):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome('chromedriver.exe', options=options)

    driver.get('http://www.foodsafetykorea.go.kr/portal/sensuousmenu/schoolMeals.do')
    driver.implicitly_wait(3)

    driver.find_element_by_xpath('//*[@id="wrap"]/main/section/div[2]/div[1]/fieldset/ul/li[2]/div/div').click()
    time.sleep(1)
    
    if local == '세종':
        driver.find_element_by_xpath('//*[@id="wrap"]/main/section/div[2]/div[1]/fieldset/ul/li[2]/div/div/div/span[8]').click()
    elif local == '서울':
        driver.find_element_by_xpath('//*[@id="wrap"]/main/section/div[2]/div[1]/fieldset/ul/li[2]/div/div/div/span[1]').click()
    elif local == '부산':
        driver.find_element_by_xpath('//*[@id="wrap"]/main/section/div[2]/div[1]/fieldset/ul/li[2]/div/div/div/span[2]').click()
    elif local == '인천':
        driver.find_element_by_xpath('//*[@id="wrap"]/main/section/div[2]/div[1]/fieldset/ul/li[2]/div/div/div/span[3]').click()
    elif local == '대구':
        driver.find_element_by_xpath('//*[@id="wrap"]/main/section/div[2]/div[1]/fieldset/ul/li[2]/div/div/div/span[4]]').click()
    elif local == '광주':
        driver.find_element_by_xpath('//*[@id="wrap"]/main/section/div[2]/div[1]/fieldset/ul/li[2]/div/div/div/span[5]').click()
    elif local == '대전':
        driver.find_element_by_xpath('//*[@id="wrap"]/main/section/div[2]/div[1]/fieldset/ul/li[2]/div/div/div/span[6]').click()
    elif local == '울산':
        driver.find_element_by_xpath('//*[@id="wrap"]/main/section/div[2]/div[1]/fieldset/ul/li[2]/div/div/div/span[7]').click()
    elif local == '경기':
        driver.find_element_by_xpath('//*[@id="wrap"]/main/section/div[2]/div[1]/fieldset/ul/li[2]/div/div/div/span[9]').click()
    elif local == '강원':
        driver.find_element_by_xpath('//*[@id="wrap"]/main/section/div[2]/div[1]/fieldset/ul/li[2]/div/div/div/span[10]').click()
    elif local == '충남':
        driver.find_element_by_xpath('//*[@id="wrap"]/main/section/div[2]/div[1]/fieldset/ul/li[2]/div/div/div/span[11]').click()
    elif local == '충북':
        driver.find_element_by_xpath('//*[@id="wrap"]/main/section/div[2]/div[1]/fieldset/ul/li[2]/div/div/div/span[12]').click()
    elif local == '경남':
        driver.find_element_by_xpath('//*[@id="wrap"]/main/section/div[2]/div[1]/fieldset/ul/li[2]/div/div/div/span[13]').click()
    elif local == '경북':
        driver.find_element_by_xpath('//*[@id="wrap"]/main/section/div[2]/div[1]/fieldset/ul/li[2]/div/div/div/span[14]').click()
    elif local == '전남':
        driver.find_element_by_xpath('//*[@id="wrap"]/main/section/div[2]/div[1]/fieldset/ul/li[2]/div/div/div/span[15]').click()
    elif local == '전북':
        driver.find_element_by_xpath('//*[@id="wrap"]/main/section/div[2]/div[1]/fieldset/ul/li[2]/div/div/div/span[16]').click()
    elif local == '제주':
        driver.find_element_by_xpath('//*[@id="wrap"]/main/section/div[2]/div[1]/fieldset/ul/li[2]/div/div/div/span[17]').click()
    else:
        print('잘못 입력했습니다.')
        driver.quit()
        main()
        return False

    time.sleep(1)
    driver.find_element_by_name('search_keyword').send_keys(school)
    driver.find_element_by_xpath('//*[@id="wrap"]/main/section/div[2]/div[1]/fieldset/ul/li[4]/a').click()

    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="listFrame"]/tr/td[4]/a[1]').click()

    print()
    print('이 급식표는 이번 주만 보여줍니다.')
    print('중식만 확인할 수 있습니다.')

    for i in range (2,7):
        day = driver.find_element_by_xpath('//*[@id="tab1"]/table/tbody/tr[%d]/td[1]' % i).text
        food_list = driver.find_element_by_xpath('//*[@id="tab1"]/table/tbody/tr[%d]/td[3]' % i).text.split(',')
        print()
        print("<< %s >>" % day)
        for menu in food_list:
            print(menu.strip())

    print()
    print(driver.find_element_by_xpath('//*[@id="wrap"]/main/section/div[2]/div[6]/span').text)
    
    driver.quit()
    return True

def main():
    local, school, grade, cla = input_information()
    while (True):
        select = input_menu()
        if select == '1':
            if (not siganpyo(school, grade, cla)):
                break
        elif select == '2':
            if (not geupsik(local, school)):
                break
        elif select == '3':
            if (not main()):
                break
            return False
        elif select == '0':
            break
        else:
            print("잘못 입력하셨습니다. 다시 입력해주세요.")
            
    return True

main()