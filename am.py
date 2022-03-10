class sql_list():
    sql_1='''
    SELECT 
        COUNT(*) 
    from oktell.dbo.armCrisis
    where city=%s and pbo=%s
        '''
    sql_2=''' 
        INSERT INTO oktell.dbo.armCrisis
        (city,pbo,adress,us,phone,fransh)
        VALUES
        (%s,%s,%s,%s,%s,%s)
           '''
    sql_3=''' 
    SELECT 
        id
    from oktell.dbo.armCrisis
    where city=%s and pbo=%s
           '''
    sql_4='''
    update oktell.dbo.armCrisis
    set
    city='{city1}',
    pbo='{pbo1}',
    adress='{adress1}',
    us='{us1}',
    phone='{phone1}',
    fransh='{fransh1}'
    where city='{city1}' and pbo='{pbo1}' 
        '''      
    sql_5=''' 
    delete oktell.dbo.armCrisis
    where id=%s
           '''



def mssql_connect(city,pbo,adress,us,phone,fransh):


    import pymssql 
    import csv



    server=
    user= 
    password=
    database=

    conn = pymssql.connect(server=server, user=user, password=password, database=database)
    cursor = conn.cursor()

    try:
        cursor.execute(sql_list.sql_1,(city,pbo)) 
        count = cursor.fetchall()
        count=list(count[0])
    except:
        cursor.close
        conn.close
        print ('error')  
        return   
    if count[0]==0:
        cursor.execute(sql_list.sql_2,(city,pbo,adress,us,phone,fransh))
        conn.commit()
        pass
    elif count[0]>1:
        cursor.execute(sql_list.sql_3,(city,pbo))
        body = cursor.fetchall()
        body=(list(body[0]))[0] 
        print (body) 
        cursor.execute(sql_list.sql_5,(body))
        conn.commit()         
        cursor.execute(sql_list.sql_4.format(city1=city,pbo1=pbo,adress1=adress,us1=us,phone1=phone,fransh1=fransh))
        conn.commit()              
    else:
        cursor.execute(sql_list.sql_4.format(city1=city,pbo1=pbo,adress1=adress,us1=us,phone1=phone,fransh1=fransh))
        conn.commit() 
        pass 
    cursor.close
    conn.close
    return 


def update(df):
    for i in df:
        city=i[0]
        pbo=i[1]
        adress=i[2]
        us=i[3]
        phone='8'+(str(i[4]).replace(' ','').replace('(','').replace(')','').replace('-','').replace('=','').replace('+7','8'))[1:]
        if i[1].find('KFC') != -1:
            fransh='KFC'
        elif  i[1].find('PH') != -1: 
            fransh='PH'    
        elif  i[1].find('РН') != -1: 
            fransh='PH'      
        mssql_connect(city,pbo,adress,us,phone,fransh)

def gooolesheet(name_sheet):
    import gspread
    gc = gspread.service_account('/home/it/sc_python/amrest/sc.json')
    secret_key=''
    wks= gc.open_by_key(secret_key)
    list_of_lists = wks.worksheet(name_sheet).get_all_records()
    return list_of_lists



def amrest():
    import pandas as pd

    names_sheet=['KFC','PH']
    for name_sheet in names_sheet:
        df =pd.DataFrame(gooolesheet(name_sheet))
        df=df.values.tolist() 
        update(df)    

    



amrest()    