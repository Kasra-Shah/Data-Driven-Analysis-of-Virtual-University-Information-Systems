import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import math
import os
pd.options.mode.chained_assignment = None  # default='warn'
def report_1(data_sesions,data_presence,data_teachers,data_courses):
    teacher = int(input("enter professor's id: "))
    while teacher not in data_teachers['prof_id'].tolist():
        print('id is wrong! try again')
        teacher = int(input("enter professor's id: "))
    teacher_classes = data_presence[data_presence['stu_prof_id']==teacher] # filter kardan bar asase teacher_id
    sesions_info = data_sesions.merge(teacher_classes,on='session_id')     # ezafe kardane zamane vorood va khorooj be dataframe ghabli
    sesions_info['presence_time'] = sesions_info['out_time']-sesions_info['in_time']    # bedast avordane zamane har jalase
    courses_info = sesions_info.groupby('course_id').agg({'presence_time':'sum','beg_time':'count'})    # majmooe zamane har cours va tedade jalasat
    report = pd.DataFrame(np.zeros((5,len(sesions_info['course_id'].unique()))),
                            index=['number of sesions','total_time','average_time','longest_time','shortest_time'],
                            columns=sesions_info['course_id'].unique())     # sakhte yek table baraye report ba values = 0
    report.columns.name='course_name'
    for i in sesions_info['course_id'].unique():                            # por kardane dataframe ba maqadire morede niaz
        report[i][0]=courses_info['beg_time'][i]
        report[i][1]=courses_info['presence_time'][i]
        report[i][2]=courses_info['presence_time'][i]/courses_info['beg_time'][i]
        cours_i = sesions_info[sesions_info['course_id']==i]
        report[i][3]=max(cours_i['presence_time'])
        report[i][4]=min(cours_i['presence_time'])
    prof_info = data_teachers[data_teachers['prof_id']==teacher]            
    print("\nteacher's id: ",teacher,'       ',"teacher's name: ",prof_info['prof_name'].tolist()[0],'       ',
            "teacher's group: ",prof_info['group'].tolist()[0])
    empty_profs = list(set(data_teachers['prof_id'])-set(data_presence['stu_prof_id']))
    if teacher in empty_profs:
        print("\nprofessor didn't have any classes this semester!")
    else:
        print('\n',report)
        
def report_2(data_sesions,data_presence,data_students):
    stu_id = int(input("enter student's id: "))
    while stu_id not in data_students['stu_id'].tolist():
        print('id is wrong! try again')
        stu_id = int(input("enter student's id: "))
    student_sesions = data_presence[data_presence['stu_prof_id']==stu_id]   # joda kardane jalasate darse daneshjoo e morede nazar
    student_sesions = data_sesions.merge(student_sesions,on='session_id')         # ezafe kardane etelate jalase
    present_sesions = student_sesions[student_sesions['in_time']!='-']          # joda kardane jalase haye hozoor dashte
    present_sesions['presence_time'] = present_sesions['out_time'] - present_sesions['in_time']  # ezafe kardane time hozoor dar jalasat
    present_sesions['late_enter'] = present_sesions['in_time']-present_sesions['beg_time']  # mohasebe takhir
    present_sesions['soon_leave'] = present_sesions['end_time']-present_sesions['out_time'] # mohasebe tarke zoodtar
    absent_sesions = student_sesions[student_sesions['in_time']=='-']
    courses_info_present = present_sesions.groupby('course_id').agg({'in_time':'count','presence_time':'sum','late_enter':'sum','soon_leave':'sum'})
    courses_info_absent = absent_sesions.groupby('course_id').agg({'beg_time':'count'})
    report = pd.DataFrame(np.zeros((5,len(student_sesions['course_id'].unique()))),         # sakhte table baraye report
                            index = ['number_of_presences','number_of_absences','total_delays','total_rushes','score'],
                            columns=student_sesions['course_id'].unique())
    for i in student_sesions['course_id'].unique():                 # por kardane table report ba maqadire morede nazar
        report[i]['number_of_presences'] = courses_info_present['in_time'][i]
        if i in list(courses_info_absent.index):                    # age darsi qeybat nadasht be jash 0 bezar
            report[i]['number_of_absences'] = courses_info_absent['beg_time'][i]
        else:
            report[i]['number_of_absences'] = 0
        report[i]['total_delays'] = courses_info_present['late_enter'][i]*60
        report[i]['total_rushes'] = courses_info_present['soon_leave'][i]*60
        report[i]['score'] = (report[i]['number_of_presences']*90)-(report[i]['total_delays'])-(report[i]['total_rushes'])
    stu_info = data_students[data_students['stu_id']==stu_id]
    report.columns.name='course_id'
    print("\nstudent's id: ",stu_id,"  student's name: ",stu_info['stu_name'].tolist()[0],"  student's major: ",stu_info['major'].tolist()[0])
    print('\n',report)

def report_3(data_sesions,data_presence,data_course):
    cours = int(input("enter course's id: "))
    while cours not in data_course['course_id'].tolist():
        print('id is wrong! try again')
        cours = int(input("enter cours's id: "))
    cours_sesions = data_sesions[data_sesions['course_id']==cours]
    cours_sesions = data_presence.merge(cours_sesions,on='session_id')      # merge kardane tamame etelaate har jalase ba afrad
    cours_sesions['total_time'] = cours_sesions['end_time']-cours_sesions['beg_time']   
    present_in_sesion = cours_sesions[cours_sesions['in_time']!='-']            # joda kardane afrade hazer ba tamame etelaat
    absent_in_sesion = cours_sesions[cours_sesions['in_time']=='-']             # joda kardane afrade ghayeb ba tamame etelaat
    all_people = cours_sesions.groupby('session_id').agg({'stu_prof_id':'count'})
    all_people['stu_prof_id'] = all_people['stu_prof_id']-1
    presence_sesion = present_in_sesion.groupby('session_id').agg({'stu_prof_id':'count'})  # mohasebe tedad afrade hazer dar har jalase
    presence_sesion['stu_prof_id'] = presence_sesion['stu_prof_id'] -1                      # yeki az tedad afrade kelas kam mikonim chon ostad made nazar nist
    absence_sesion = absent_in_sesion.groupby('session_id').agg({'stu_prof_id':'count'})    # mohasebe tedad afrade qayeb dar har kelas
    total_time = data_sesions.groupby('course_id').agg({'beg_time':'sum','end_time':'sum'}) # mohasebe kole zamane har cours
    total_time['total_time'] = total_time['end_time']-total_time['beg_time']                # mohasebe kole zamane har cours
    cours_info = data_course[data_course['course_id']==cours]
    report = pd.Series(np.zeros(7),index=[                  # sakhte yek serie baraye gozaresh
    'number_of_sesions',
    'average_number_of_presents',
    'average_number_of_absents',
    'max_number_of_presents',
    'max_number_of_absents',
    'total_times_of_sesions',
    'average_sesion_time'])
    report['number_of_sesions'] = len(cours_sesions['session_id'].unique())     # mohasebe tedad jalasate dars
    report['average_number_of_presents'] = sum(presence_sesion['stu_prof_id'])/report['number_of_sesions']
    report['average_number_of_absents'] = sum(absence_sesion['stu_prof_id'])/report['number_of_sesions']
    report['max_number_of_presents'] = max(presence_sesion['stu_prof_id'])
    report['max_number_of_absents'] = max(absence_sesion['stu_prof_id'])
    report['total_times_of_sesions'] = total_time['total_time'][cours]
    report['average_sesion_time'] = report['total_times_of_sesions']/report['number_of_sesions']
    print("\ncourse id: ",cours,"     course name: ",cours_info['course_name'].tolist()[0])
    print('\n',report,'\n')
                                                            ####### baraye darsayi ke qayeb nadaran error mide

def report_4(data_sesions,data_presence,data_course,data_teachers):
        cours = int(input("enter course's id: "))
        while cours not in data_course['course_id'].tolist():
            print('id is wrong! try again')
            cours = int(input("enter cours's id: "))
        cours_sesions = data_sesions[data_sesions.loc[:,('course_id')]==cours]
        cours_sesions['total_time'] = cours_sesions['end_time']-cours_sesions['beg_time']
        #print('\ncours id: ',cours,'      cours name: ',(data_course[data_course['course_id']==cours])['course_name'].tolist()[0])
        sesions_info = data_sesions.merge(data_presence,on='session_id')
        cours_sesions_all=sesions_info[sesions_info['course_id']==cours]
        prof_info = data_teachers[data_teachers['prof_id']==cours_sesions_all['stu_prof_id'].tolist()[0]]
        titlee = str('cours id: '+str(cours)+'      cours name: '+str((data_course[data_course['course_id']==cours])['course_name'].tolist()[0])+
            '\nprof id: '+str(prof_info['prof_id'].tolist()[0])+'      prof name: '+str(prof_info['prof_name'].tolist()[0]))
        cours_sesions.plot.bar(x='date',y='total_time',title=titlee,color='tan')
        plt.show()

def report_5(data_sesions,data_presence,data_course,data_teacher):
    prof_id = int(input("enter teacher's id: "))
    while prof_id not in data_teacher['prof_id'].tolist():
        print('id is wrong! try again')
        prof_id = int(input("enter professor's id: "))
    teacher_classes = data_presence[data_presence['stu_prof_id']==prof_id] # filter kardan bar asase teacher_id
    sesions_info = data_sesions.merge(teacher_classes,on='session_id')     # ezafe kardane zamane vorood va khorooj be dataframe ghabli
    sesions_info = sesions_info.drop(['date','in_time','out_time'],axis=1)
    sesions_info['total_time'] = sesions_info['end_time']-sesions_info['beg_time']
    cours_sum = sesions_info.groupby('course_id').agg({'total_time':'sum','stu_prof_id':'count'})
    coruses_info = data_course[data_course['course_id'].isin(cours_sum.index.values.tolist())]
    cours_sum = cours_sum.merge(coruses_info,on='course_id')
    cours_sum['value'] = cours_sum['total_time']/(cours_sum['stu_prof_id']*cours_sum['unit']*45)
    prof_info = data_teacher[data_teacher['prof_id']==prof_id]       
    titlee = str('teacher id: '+str(prof_id)+'      teacher name: '+str(prof_info['prof_name'].tolist()[0]))   
    cours_sum['value'].plot.pie(labels=cours_sum['course_id'].tolist(),
                                autopct='%.2f',
                                title=titlee)
    plt.show()

def report_6(data_teacher,data_presence,data_sesions):
    teacher_ids = []
    print('enter id of profesors: (after every id press enter and if you entered all, enter 0 to see the report')
    id = 1
    while len(teacher_ids)<21 and id!=0:
        id = int(input('id :'))
        if id == 0:
            break
        if id in data_teacher['prof_id'].tolist():
            if id not in teacher_ids:
                teacher_ids.append(id)
        else:
            print('id is wrong! try again')
            continue
    teacher_ids = pd.DataFrame(teacher_ids,columns=['prof_id'])
    data = data_presence[data_presence['stu_prof_id'].isin(teacher_ids['prof_id'].tolist())]
    data = data.merge(data_sesions,on='session_id')
    data['total_time'] = data['out_time']-data['in_time']
    data =data.drop(['beg_time','end_time','date','out_time','in_time'],axis=1)
    courses_time = data.groupby('course_id').agg({'total_time':'sum'})
    zero_df = pd.DataFrame(np.zeros((len(courses_time['total_time'].tolist()),len(courses_time['total_time'].tolist()))),
                            columns=courses_time.index.values.tolist())
    zero_df['prof_id']=teacher_ids['prof_id']
    teacher_ids = teacher_ids.merge(zero_df,on='prof_id')
    data_unique = data.drop_duplicates(subset=['stu_prof_id','course_id']).drop(['session_id','total_time'],axis=1)
    data_unique=data_unique.merge(courses_time,on='course_id')
    report = data_unique.pivot(index='stu_prof_id',columns='course_id',values='total_time')#.fillna(0)
    cours_count = data_unique.groupby('stu_prof_id').agg({'course_id':'count'})
    report.plot.bar(stacked=True)
    print(data_unique)
    print(cours_count)
    print(report)
    plt.show()

def report_7(data_students,data_presence,data_sesions,):
    stu_ids = []
    print('enter id of students: (after every id press enter and if you entered all, enter 0 to see the report')
    id = 1
    while len(stu_ids)<39 and id!=0:
        id = int(input('id :'))
        if id == 0:
            break
        if id in data_students['stu_id'].tolist():
            if id not in stu_ids:
                stu_ids.append(id)
        else:
            print('id is wrong! try again')
            continue
    stu_ids = pd.DataFrame(stu_ids,columns=['stu_id'])
    data = data_presence[data_presence['stu_prof_id'].isin(stu_ids['stu_id'].tolist())]
    data = data.merge(data_sesions.drop(['date','beg_time','end_time'],axis=1))
    data_unique = data.drop_duplicates(subset=['stu_prof_id','course_id'])
    print(data.head())

def report_8(data_presence,data_sesions,data_students,data_course,data_teacher):
    absents = data_presence[data_presence['in_time']=='-']
    absents = data_sesions.merge(absents,on='session_id')
    absents = absents.rename(columns={'stu_prof_id':'stu_id'})
    absents = absents.merge(data_students,on='stu_id')
    absents = absents.merge(data_course,on='course_id')
    absents=absents.drop(['session_id','date','beg_time','end_time','out_time','major','unit'],axis=1)
    absents_info = absents.groupby(['course_name','stu_name']).agg({'in_time':'count'})
    absents_info = absents_info[absents_info['in_time']>4]
    report = absents_info.unstack().transpose()
    report = report.droplevel(0,axis=0)
    report1 = np.array(report.columns.values)
    for i in report.columns.values:
        for j in report.index.values:
            if math.isnan(report[i][j])== False:
               report[i][j] = j
    final_report = np.vstack((report1,report.values))
    profs = list(set(data_teacher['prof_id'])-set(data_presence['stu_prof_id']))
    profs_name=[]
    for i in profs:
        j = data_teacher[data_teacher['prof_id']==i]
        profs_name.append(j['prof_name'].tolist()[0])
    profs_name = np.array(profs_name).reshape(len(profs),1)
    final_report = pd.DataFrame(final_report)
    profs_name = pd.DataFrame(profs_name)
    with pd.ExcelWriter('Report_8.xlsx') as writer:
        final_report.to_excel(writer,sheet_name='sheet1')
        profs_name.to_excel(writer,sheet_name='sheet2')

def main_code():
    os.system('cls'or'clear')
    teachers = pd.read_excel('database.xlsx',sheet_name='Sheet1')
    courses = pd.read_excel('database.xlsx',sheet_name='Sheet3')
    students = pd.read_excel('database.xlsx',sheet_name='Sheet2')
    sesions = pd.read_excel('database.xlsx',sheet_name='Sheet4')
    presence = pd.read_excel('database.xlsx',sheet_name='Sheet5')
    command = 0
    while command != 'q':
        print('\n----------- menu -----------',
              '\nprofessor in each cours:    1',
              '\nstudent in each cours:      2',
              '\ncours:                      3'
              '\nbar chart for cours:        4',
              '\npie chart for professor:    5',
              '\ncomulative bar chart:       6',
              '\nscatter chart:              7',
              '\nexcel report:               8'
              '\nexit:                       q')
        command = input('\nenter a command number: ')
        os.system('cls'or'clear')
        if command == '1':
            report_1(sesions,presence,teachers,courses)
        elif command == '2':
            report_2(sesions,presence,students)
        elif command == '3':
            report_3(sesions,presence,courses)
        elif command == '4':
            report_4(sesions,presence,courses,teachers)
        elif command == '5':
            report_5(sesions,presence,courses,teachers)
        elif command == '6':
            report_6(teachers,presence,sesions)
        elif command == '7':
            report_7(students,presence,sesions)
        elif command == '8':
            report_8(presence,sesions,students,courses,teachers)

main_code()
