#!/usr/bin/env python
# coding: utf-8

# # Event Frac Visualization Model 
# 
# ### by Joseph Kenrick
# 
# #### This code brings in Event data from Pinnacle Event Reports, generating the equation of a circle for each event and visualizes them in 3D space. It also plot's each Diatomite layer across the field and each wellbore and perforation interval. The Summary Table includes metrics to describe the behaviors and properties of the Event Fracs, and how they interect with nearby Wellbores.
# 

# In[190]:


# What Asset to generate models for?
assetcount=0
Assets=['KKSCW','EMRMZ','MCK']
while assetcount < len(Assets):
    Asset = Assets[assetcount]
        
    # In[191]:
    
    
    #pip install plotly
    
    
    # In[192]:
    
    
    import plotly.offline as pyo
    import plotly.graph_objs as go
    import plotly.express as px
    # Set notebook mode to work in offline
    #pyo.init_notebook_mode()
    import plotly.io as pio
    import numpy as np
    import pandas as pd
    import random
    from random import seed
    from statistics import mean
    import pyodbc
    pd.set_option('display.max_columns', None)
    #pd.set_option('display.max_rows', None)
    import re
    
    
    # In[193]:
    
    
    query1 = """SELECT EventDetailsID
          ,EventID
          ,enddate
          ,fracture_md
          ,frac_diameter
          ,x_nad27
          ,y_nad27
          ,azimuth
          ,dip_direction
          ,dip_magnitude
          ,comments
          ,EventType
          ,TopOfDiatomite
      FROM PINNACLE_EventDetails WITH (NOLOCK)
    
      Where EventType='FinalEvent' AND
      enddate > '12/31/2017'
      order by enddate desc"""
     
    query2 = """SELECT vwOfmHeader_CA.wellzonenum
          ,vwOfmHeader_CA.API_No
          ,vwOfmHeader_CA.ALIAS
          ,vwOfmHeader_CA.XCOORD_SURF
          ,vwOfmHeader_CA.YCOORD_SURF
          ,vwOfmHeader_CA.XCOORD_COMP
          ,vwOfmHeader_CA.YCOORD_COMP
          ,vwOfmHeader_CA.XCOORD_BH
          ,vwOfmHeader_CA.YCOORD_BH
          ,vwOfmHeader_CA.LATNAD83
          ,vwOfmHeader_CA.LONGNAD83
          ,vwOfmHeader_CA.GROUND_ELEV
          ,vwOfmHeader_CA.WELL_NAME
          ,vwOfmHeader_CA.COMPL_NAME
          ,vwOfmHeader_CA.REG_NAME
          ,vwOfmHeader_CA.WELL_SYMBOL
          ,vwOfmHeader_CA.TVD
    	  ,vwOfmFilterData.ASSET
          ,vwOfmFilterData.FIELD
          ,vwOfmFilterData.LEASE
          ,vwOfmFilterData.ZONE
          ,vwOfmFilterData.DRILL_YEAR
          ,vwOfmFilterData.COMPL_YEAR
          ,vwOfmFilterData.ABAND_YEAR
          ,vwOfmFilterData.TopPerf
    
      FROM vwOfmHeader_CA WITH (NOLOCK)
    	JOIN vwOfmFilterData WITH (NOLOCK) ON vwOfmHeader_CA.wellzonenum = vwOfmFilterData.wellzonenum
    
    WHERE vwOfmFilterData.OPERATOR='SPR'"""
    
    query3 = """SELECT [PINNACLE_EventDetails].[EventDetailsID]
      ,[PINNACLE_EventDetails].[EventID]
      ,[PINNACLE_EventDetails].[enddate]
      ,[PINNACLE_EventDetails].[fracture_md]
      ,[PINNACLE_EventDetails].[x_nad27]
      ,[PINNACLE_EventDetails].[y_nad27]
      ,[PINNACLE_EventDetails].[comments]
      ,[PINNACLE_EventDetails].[EventType]
      ,[PINNACLE_EventDetails].[TopOfDiatomite]
	  ,[PINNACLE_Wells].[suspect_api14]
	  ,[vwOfmHeader_CA].[WELL_NAME]
      ,[PINNACLE_Wells].[WellDataType]
      ,[PINNACLE_Events].[assetid]
      ,[PINNACLE_Events].[eventname]
      ,[PINNACLE_EventFiles].[Filename]
      ,[PINNACLE_EventFiles].[FileURL]
      
    FROM [Pinnacle].[dbo].[PINNACLE_EventDetails]
	JOIN [Pinnacle].[dbo].[PINNACLE_Wells] ON [Pinnacle].[dbo].[PINNACLE_Wells].[EventDetailsID] = [Pinnacle].[dbo].[PINNACLE_EventDetails].[EventDetailsID]
	JOIN [Pinnacle].[dbo].[PINNACLE_Events] ON [Pinnacle].[dbo].[PINNACLE_Events].[EventID] = [Pinnacle].[dbo].[PINNACLE_EventDetails].[EventID]
	LEFT JOIN [Pinnacle].[dbo].[PINNACLE_EventFiles] ON [Pinnacle].[dbo].[PINNACLE_EventFiles].[EventID] = [Pinnacle].[dbo].[PINNACLE_EventDetails].[EventID] AND [PINNACLE_EventFiles].[Filename] LIKE '%Final%'
	LEFT JOIN [OFM].[dbo].[vwOfmHeader_CA] ON SUBSTRING([OFM].[dbo].[vwOfmHeader_CA].[API_No],1,10) = CONCAT('0',SUBSTRING([Pinnacle].[dbo].[PINNACLE_Wells].[suspect_api14],1,9))

  Where [PINNACLE_EventDetails].[EventType]='FinalEvent' AND 
  [PINNACLE_Wells].WellDataType='source_wells' AND
  [PINNACLE_EventDetails].[enddate] > '12/31/2017'
      order by [PINNACLE_EventDetails].enddate desc"""
      
    query4="""SELECT [PINNACLE_EventDetails].[EventDetailsID]
      ,[PINNACLE_EventDetails].[EventID]
      ,[PINNACLE_EventDetails].[enddate]
      ,[PINNACLE_EventDetails].[fracture_md]
      ,[PINNACLE_EventDetails].[x_nad27]
      ,[PINNACLE_EventDetails].[y_nad27]
      ,[PINNACLE_EventDetails].[comments]
      ,[PINNACLE_EventDetails].[EventType]
      ,[PINNACLE_EventDetails].[TopOfDiatomite]
	  ,[PINNACLE_Wells].[suspect_api14]
	  ,[vwOfmHeader_CA].[WELL_NAME]
      ,[PINNACLE_Wells].[WellDataType]
      ,[PINNACLE_Events].[assetid]
      ,[PINNACLE_Events].[eventname]
      ,[PINNACLE_EventFiles].[Filename]
      ,[PINNACLE_EventFiles].[FileURL]
      
    FROM [Pinnacle].[dbo].[PINNACLE_EventDetails]
	JOIN [Pinnacle].[dbo].[PINNACLE_Wells] ON [Pinnacle].[dbo].[PINNACLE_Wells].[EventDetailsID] = [Pinnacle].[dbo].[PINNACLE_EventDetails].[EventDetailsID]
	JOIN [Pinnacle].[dbo].[PINNACLE_Events] ON [Pinnacle].[dbo].[PINNACLE_Events].[EventID] = [Pinnacle].[dbo].[PINNACLE_EventDetails].[EventID]
	LEFT JOIN [Pinnacle].[dbo].[PINNACLE_EventFiles] ON [Pinnacle].[dbo].[PINNACLE_EventFiles].[EventID] = [Pinnacle].[dbo].[PINNACLE_EventDetails].[EventID] AND [PINNACLE_EventFiles].[Filename] LIKE '%Final%'
	LEFT JOIN [OFM].[dbo].[vwOfmHeader_CA] ON SUBSTRING([OFM].[dbo].[vwOfmHeader_CA].[API_No],1,10) = CONCAT('0',SUBSTRING([Pinnacle].[dbo].[PINNACLE_Wells].[suspect_api14],1,9))

  Where [PINNACLE_EventDetails].[EventType]='FinalEvent' AND 
  [PINNACLE_Wells].WellDataType='source_candidate_wells' AND
  [PINNACLE_EventDetails].[enddate] > '12/31/2017'
      order by [PINNACLE_EventDetails].enddate desc"""
      
    query5="""SELECT [PINNACLE_EventDetails].[EventDetailsID]
          ,[PINNACLE_EventDetails].[EventID]
          ,[PINNACLE_EventDetails].[enddate]
          ,[PINNACLE_EventDetails].[fracture_md]
          ,[PINNACLE_EventDetails].[x_nad27]
          ,[PINNACLE_EventDetails].[y_nad27]
          ,[PINNACLE_EventDetails].[comments]
          ,[PINNACLE_EventDetails].[EventType]
          ,[PINNACLE_EventDetails].[TopOfDiatomite]
    	  ,[PINNACLE_Wells].[suspect_api14]
    	  ,[vwOfmHeader_CA].[WELL_NAME]
          ,[PINNACLE_Wells].[WellDataType]
          ,[PINNACLE_Events].[assetid]
          ,[PINNACLE_Events].[eventname]
          ,[PINNACLE_EventFiles].[Filename]
          ,[PINNACLE_EventFiles].[FileURL]
          
        FROM [Pinnacle].[dbo].[PINNACLE_EventDetails]
    	JOIN [Pinnacle].[dbo].[PINNACLE_Wells] ON [Pinnacle].[dbo].[PINNACLE_Wells].[EventDetailsID] = [Pinnacle].[dbo].[PINNACLE_EventDetails].[EventDetailsID]
    	JOIN [Pinnacle].[dbo].[PINNACLE_Events] ON [Pinnacle].[dbo].[PINNACLE_Events].[EventID] = [Pinnacle].[dbo].[PINNACLE_EventDetails].[EventID]
    	LEFT JOIN [Pinnacle].[dbo].[PINNACLE_EventFiles] ON [Pinnacle].[dbo].[PINNACLE_EventFiles].[EventID] = [Pinnacle].[dbo].[PINNACLE_EventDetails].[EventID] AND [PINNACLE_EventFiles].[Filename] LIKE '%Final%'
    	LEFT JOIN [OFM].[dbo].[vwOfmHeader_CA] ON SUBSTRING([OFM].[dbo].[vwOfmHeader_CA].[API_No],1,10) = CONCAT('0',SUBSTRING([Pinnacle].[dbo].[PINNACLE_Wells].[suspect_api14],1,9))
    
      Where [PINNACLE_EventDetails].[EventType]='FinalEvent' AND 
      [PINNACLE_Wells].WellDataType='suspect_wells' AND
      [PINNACLE_EventDetails].[enddate] > '12/31/2017'
          order by [PINNACLE_EventDetails].enddate desc"""
    
    
    # In[194]:
    
    
    conn1 = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server=SQL01-PROD;'
                          'Database=Pinnacle;'
                          'Trusted_Connection=yes;'
                          'MARS_Connection=yes;')
    
    cursor1 = conn1.cursor()
    cursor1.execute(query1)
    
    sql_query = pd.read_sql_query(query1,conn1)
    sql_query['comments']=sql_query['comments'].replace(to_replace=np.nan,value="NaN")
    
    conn2 = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server=SQL01-PROD;'
                          'Database=OFM;'
                          'Trusted_Connection=yes;'
                          'MARS_Connection=yes;')
    
    cursor2 = conn2.cursor()
    cursor2.execute(query2)
    
    wellbore_df = pd.read_sql_query(query2,conn2)
    
    conn3 = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=SQL01-PROD;'
                      'Database=Pinnacle;'
                      'Trusted_Connection=yes;'
                      'MARS_Connection=yes;')

    cursor3 = conn1.cursor()
    cursor3.execute(query1)
    
    source_query = pd.read_sql_query(query3,conn3)
    source_query['comments']=source_query['comments'].replace(to_replace=np.nan,value="NaN")
    
    conn4 = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=SQL01-PROD;'
                      'Database=Pinnacle;'
                      'Trusted_Connection=yes;'
                      'MARS_Connection=yes;')

    cursor4 = conn4.cursor()
    cursor4.execute(query4)
    
    candidatewells = pd.read_sql_query(query4,conn4)
    
    conn5 = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server=SQL01-PROD;'
                          'Database=Pinnacle;'
                          'Trusted_Connection=yes;'
                          'MARS_Connection=yes;')
    
    cursor5 = conn5.cursor()
    cursor5.execute(query5)
    
    suspectwells = pd.read_sql_query(query5,conn5)
    
    conn1.close()
    conn2.close()
    conn3.close()
    conn4.close()
    conn5.close()
    
    # In[195]:
    
    
    i=0
    while i < len(wellbore_df['WELL_NAME']):
        if(wellbore_df['REG_NAME'][i] is None):
                wellbore_df['REG_NAME'][i]=wellbore_df['WELL_NAME'][i]
        try:        
            if(wellbore_df['WELL_NAME'][i][0:4]=="19Z "):
                    wellbore_df['WELL_NAME'][i]=wellbore_df['WELL_NAME'][i].replace(" ","-")
            if(wellbore_df['COMPL_NAME'][i][0:4]=="19Z "):
                    wellbore_df['COMPL_NAME'][i]=wellbore_df['COMPL_NAME'][i].replace(" ","-")        
            if(wellbore_df['REG_NAME'][i][0:4]=="19Z "):
                    wellbore_df['REG_NAME'][i]=wellbore_df['REG_NAME'][i].replace(" ","-")
        except:
            wellbore_df.drop(i,inplace=True)
        i=i+1
        
    wellbore_df=wellbore_df.sort_values('TopPerf',ascending = True)
    wellbore_df=wellbore_df.reset_index()
    wellbore_df=wellbore_df.drop(['index'],axis=1)
    wellbore_df['DRILL_YEAR']=wellbore_df['DRILL_YEAR'].replace(to_replace='UNKNOWN',value=-1)
    wellbore_df['DRILL_YEAR']=wellbore_df['DRILL_YEAR'].astype(float)
    
    wellbore_df['XCOORD_BH']=wellbore_df['XCOORD_BH'].astype('str')
    wellbore_df['XCOORD_BH']=wellbore_df['XCOORD_BH'].replace("nan",-1)
    wellbore_df['XCOORD_BH']=wellbore_df['XCOORD_BH'].astype('float')
    
    
    # In[196]:
    
    
    if Asset =='KKSCW':
        KKSCW_data=sql_query[sql_query['x_nad27']>1540000]
        KKSCW_data=KKSCW_data[KKSCW_data['x_nad27']<1555000]
        KKSCW_data=KKSCW_data[KKSCW_data['y_nad27']>590000]
        KKSCW_data=KKSCW_data[KKSCW_data['y_nad27']<602000]
        KKSCW_data.reset_index(inplace=True)
        KKSCW_data=KKSCW_data.drop(['index'],axis=1)
        Leasewellbore_df=wellbore_df[wellbore_df['XCOORD_SURF']>1540000]
        Leasewellbore_df=Leasewellbore_df[Leasewellbore_df['XCOORD_SURF']<1555000]
        Leasewellbore_df=Leasewellbore_df[Leasewellbore_df['YCOORD_SURF']>590000]
        Leasewellbore_df=Leasewellbore_df[Leasewellbore_df['YCOORD_SURF']<602000]
        Leasewellbore_df.reset_index(inplace=True)
        Leasewellbore_df=Leasewellbore_df.drop(['index'],axis=1)
        Lease_data=KKSCW_data.copy()
        Fields=['KEENE','KELLY','SOUTH CERRITOS','WILLIAMS']
        path3 = r'\\fs01.sentinelpeakresources.local\I Drive\Assets\SJV\Frac_Model_HTML\Additional Layers\KKSCW STRUCTURE_MD_POINTS Cropped.xlsx'
        welllist=wellbore_df[wellbore_df['LEASE'].isin(Fields)]
        
    if Asset == 'MCK':
        MCK_data=sql_query[sql_query['x_nad27']>1507000]
        MCK_data=MCK_data[MCK_data['x_nad27']<1512000]
        MCK_data=MCK_data[MCK_data['y_nad27']>659000]
        MCK_data=MCK_data[MCK_data['y_nad27']<664000]
        MCK_data.reset_index(inplace=True)
        MCK_data=MCK_data.drop(['index'],axis=1)
        Leasewellbore_df=wellbore_df[wellbore_df['XCOORD_SURF']>1507000]
        Leasewellbore_df=Leasewellbore_df[Leasewellbore_df['XCOORD_SURF']<1512000]
        Leasewellbore_df=Leasewellbore_df[Leasewellbore_df['YCOORD_SURF']>659000]
        Leasewellbore_df=Leasewellbore_df[Leasewellbore_df['YCOORD_SURF']<664000]
        Leasewellbore_df.reset_index(inplace=True)
        Leasewellbore_df=Leasewellbore_df.drop(['index'],axis=1)
        Lease_data=MCK_data.copy()
        Fields=['MCKITTRICK']
        path3 = r'\\fs01.sentinelpeakresources.local\I Drive\Assets\SJV\Frac_Model_HTML\Additional Layers\19Z STRUCTURE_MD_POINTS.xlsx'
        i=0
        while i < len(Lease_data):
            if('19Z ' in Lease_data['comments'][i]):
                Lease_data['comments'][i]=Lease_data['comments'][i].replace('19Z ','19Z-') 
            i=i+1
        welllist=wellbore_df[wellbore_df['FIELD'].isin(Fields)]
        welllist=welllist[welllist['ZONE']=='DIATOMITE']
        
    #CYM_data=sql_query[sql_query['x_nad27']>1499000]
    #CYM_data=CYM_data[CYM_data['x_nad27']<1508000]
    #CYM_data=CYM_data[CYM_data['y_nad27']>670000]
    #CYM_data=CYM_data[CYM_data['y_nad27']<682000]
    #CYM_data.reset_index(inplace=True)
    #CYM_data=CYM_data.drop(['index'],axis=1)
    
    if Asset == 'EMRMZ':
        EMRMZ_data=sql_query[sql_query['x_nad27']>1520000]
        EMRMZ_data=EMRMZ_data[EMRMZ_data['x_nad27']<1530000]
        EMRMZ_data=EMRMZ_data[EMRMZ_data['y_nad27']<652000]
        EMRMZ_data=EMRMZ_data[EMRMZ_data['y_nad27']>635000]
        EMRMZ_data.reset_index(inplace=True)
        EMRMZ_data=EMRMZ_data.drop(['index'],axis=1)
        Leasewellbore_df=wellbore_df[wellbore_df['XCOORD_SURF']>1520000]
        Leasewellbore_df=Leasewellbore_df[Leasewellbore_df['XCOORD_SURF']<1530000]
        Leasewellbore_df=Leasewellbore_df[Leasewellbore_df['YCOORD_SURF']<652000]
        Leasewellbore_df=Leasewellbore_df[Leasewellbore_df['YCOORD_SURF']>635000]
        Leasewellbore_df.reset_index(inplace=True)
        Leasewellbore_df=Leasewellbore_df.drop(['index'],axis=1)
        Lease_data=EMRMZ_data.copy()
        Fields=['E AND M','REARDON','MAGEE','34Z WEST','34Z EAST']
        path3= r'\\fs01.sentinelpeakresources.local\I Drive\Assets\SJV\Frac_Model_HTML\Additional Layers\EM_RMZ TOD MD.xlsx'
        welllist=wellbore_df[wellbore_df['LEASE'].isin(Fields)]
    
    welllist=welllist[welllist['WELL_SYMBOL']!="UNK"]
    welllist=welllist.sort_values('WELL_NAME')
    welllist=welllist['WELL_NAME']
    welllist.drop_duplicates(inplace=True)
    welllist=welllist.reset_index()
    welllist=welllist.drop(['index'],axis=1)
    
    
    # In[197]:
    
    
    allwells=Leasewellbore_df[Leasewellbore_df['WELL_SYMBOL']!="UNK"].copy()
    allwells=allwells[['WELL_NAME','REG_NAME','ALIAS']]
    allwells=allwells.sort_values('WELL_NAME')
    allwells=allwells.reset_index()    
    allwells=allwells.drop(['index'],axis=1)
    allwells['ALIAS']=allwells['ALIAS'].astype('str')
    allwells['ALIAS2']=np.nan
    i=0
    while i <len(allwells):
        if(len(re.findall(r'\D',allwells['ALIAS'][i]))==0):
            allwells['ALIAS'][i]=allwells['REG_NAME'][i]
        if(len(allwells['ALIAS'][i])<3):
            allwells['ALIAS'][i]=allwells['REG_NAME'][i]
        if(allwells['ALIAS'][i][-1]=='D'):
            allwells['ALIAS2'][i]=allwells['ALIAS'][i].replace('D','')
        else:
            allwells['ALIAS2'][i]=allwells['ALIAS'][i]
        i=i+1
    allwells.drop_duplicates(inplace=True)
    allwells=allwells.reset_index()
    allwells=allwells.drop(['index'],axis=1)
    
    
    # In[198]:
    
    #source candidate well selection
    candidatewells=candidatewells.drop_duplicates()
    candidatewells.reset_index(inplace=True)
    maxcandidates=np.array(candidatewells['EventDetailsID'].value_counts())[0]
    i=1
    while i < maxcandidates+1:
        source_query['Source Candidate Well ' + str(i)]=np.nan
        source_query['Source Candidate Well ' + str(i)]=source_query['Source Candidate Well ' + str(i)].astype('str')
        i=i+1
    
    suspectwells=suspectwells.drop_duplicates()
    suspectwells.reset_index(inplace=True)
    maxsuspects=np.array(suspectwells['EventDetailsID'].value_counts())[0]
    i=1
    while i < maxsuspects+1:
        source_query['Source Suspect Well ' + str(i)]=np.nan
        source_query['Source Suspect Well ' + str(i)]=source_query['Source Suspect Well ' + str(i)].astype('str')
        i=i+1
    
    candidatewells=candidatewells.fillna(np.nan)
    candidatewells=candidatewells.replace("None",np.nan)
    candidatewells=candidatewells.replace("Nothing",np.nan)
    candidatewells=candidatewells.replace(np.nan,-1)
    suspectwells=suspectwells.fillna(np.nan)
    suspectwells=suspectwells.replace("None",np.nan)
    suspectwells=suspectwells.replace("Nothing",np.nan)
    suspectwells=suspectwells.replace(np.nan,-1)
    
    i=0
    while i < len(source_query):
        event=source_query['EventDetailsID'][i]
        k=0
        while k < len(candidatewells):
            if candidatewells['EventDetailsID'][k]==event:
                if (candidatewells['WELL_NAME'][k]==-1):
                    source_query.at[i,'Source Candidate Well 1']=candidatewells['suspect_api14'][k]
                else:
                    source_query.at[i,'Source Candidate Well 1']=candidatewells['WELL_NAME'][k]
                k=k+1
                if k < len(candidatewells):
                    j=0
                    while j < maxcandidates-1:
                        if (k+j)<len(candidatewells):
                            if candidatewells['EventDetailsID'][k+j]==event:
                                if (candidatewells['WELL_NAME'][k+j]==-1):
                                    source_query.at[i,'Source Candidate Well '+str(j+2)]=candidatewells['suspect_api14'][k+j]
                                else:
                                    source_query.at[i,'Source Candidate Well '+str(j+2)]=candidatewells['WELL_NAME'][k+j]
                                j=j+1
                            else:
                                k=k+j
                                j=maxcandidates
                        else:
                            j=maxcandidates
            else:
                k=k+1
        i=i+1
        
    i=0
    while i < len(source_query):
        event=source_query['EventDetailsID'][i]
        k=0
        while k < len(suspectwells):
            if suspectwells['EventDetailsID'][k]==event:
                if (suspectwells['WELL_NAME'][k]==-1):
                    source_query.at[i,'Source Suspect Well 1']=suspectwells['suspect_api14'][k]
                else:
                    source_query.at[i,'Source Suspect Well 1']=suspectwells['WELL_NAME'][k]
                k=k+1
                if k < len(suspectwells):
                    j=0
                    while j < maxsuspects-1:
                        if k+j<len(suspectwells):
                            if suspectwells['EventDetailsID'][k+j]==event:
                                if (suspectwells['WELL_NAME'][k+j]==-1):
                                    source_query.at[i,'Source Suspect Well '+str(j+2)]=suspectwells['suspect_api14'][k+j]
                                else:
                                    source_query.at[i,'Source Suspect Well '+str(j+2)]=suspectwells['WELL_NAME'][k+j]                    
                                j=j+1
                            else:
                                k=k+j
                                j=maxsuspects
                        else:
                            j=maxsuspects
            else:
                k=k+1
        i=i+1
                        
    source_query['Source Well']=np.nan
    source_query['Source Well']=source_query['Source Well'].astype('str')
    source_query=source_query.fillna(np.nan)
    source_query=source_query.replace("None",np.nan)
    source_query=source_query.replace("Nothing",np.nan)
    source_query=source_query.replace(np.nan,-1)
    
    i=0
    while i < len(source_query):
        if source_query['WELL_NAME'][i]==-1:
            if source_query['suspect_api14'][i]==-1:
                if source_query['Source Candidate Well 1'][i]==-1:
                    if source_query['Source Suspect Well 1'][i]==-1:
                        source_query.at[i,'Source Well']=-1
                    else:
                        source_query.at[i,'Source Well']=source_query['Source Suspect Well 1'][i]
                else:
                    source_query.at[i,'Source Well']=source_query['Source Candidate Well 1'][i]
            else:
                source_query.at[i,'Source Well']=source_query['suspect_api14'][i]
        else:
            source_query.at[i,'Source Well']=source_query['WELL_NAME'][i]
        i=i+1        
    
    source_query=source_query.drop_duplicates()
    source_query=source_query.reset_index()
    source_query=source_query.drop('index',axis=1)
    source_query['Source Well']=source_query['Source Well'].replace('nan',-1)
    
    
    #source candidate well search in text
    column_names= ['Event Start','Event End','Depth','Strike Azimuth','Dip','Estimated Event Diameter','NAD27 Easting','NAD27 Northing','Source Well','Top Perf','Asset','Field','Lease','Drill Year','X_Surf','Y_Surf','X_BH','Y_BH','TOD']
    Leaseevent_df = pd.DataFrame(columns = column_names)
    
    i = 0
    while i < len(Lease_data):           
        #Event Start and Ends
        TOD=-Lease_data['TopOfDiatomite'][i]
        comment=Lease_data['comments'][i]
        if comment=="NaN":
            Event_Start=np.nan
        elif comment.split(" was",1)[0]=="2017/XX/XXX":
            Event_Start=np.nan
        else:
            try:
                if (comment.split("Event ",1)[1]==comment.split("Event ",1)[1].split(" ended as ",1)[0]):
                    if(comment.split("Event ",1)[1]==comment.split("Event ",1)[1].split("terminated ",1)[0]):
                        if(comment.split("Event ",1)[1]==comment.split("Event ",1)[1].split(" started ",1)[0]):
                            if(comment.split("Event ",1)[1]==comment.split("Event ",1)[1].split(" terminaed ",1)[0]):
                                Event_Start = comment.split("Event ",1)[1].split(" began ",1)[0]
                            else:
                                Event_Start=comment.split("Event ",1)[1].split(" terminaed ",1)[0]
                        else:
                            Event_Start = comment.split("Event ",1)[1].split(" started ",1)[0]
                    else:
                        Event_Start = comment.split("Event ",1)[1].split(" terminated ",1)[0]
                else:
                    Event_Start = comment.split("Event ",1)[1].split(" ended as ",1)[0]
            except:
                Event_Start = np.nan
                
        if(Event_Start==np.nan):
            Event_Start=Event_Start
        else:
            try:
                if (Event_Start==Event_Start.split("E",1)[0]): 
                    if (Event_Start==Event_Start.split("D",1)[0]):    
                        if (Event_Start==Event_Start.split("C",1)[0]):
                            if (Event_Start==Event_Start.split("B",1)[0]):
                                Event_Start = Event_Start.split("A",1)[0]
                            else:
                                Event_Start=Event_Start.split("B",1)[0]
                        else:
                            Event_Start = Event_Start.split("C",1)[0]
                    else:
                        Event_Start = Event_Start.split("D",1)[0]
                else:
                    Event_Start = Event_Start.split("E",1)[0]
            except:
                Event_Start=Event_Start
        
        Event_Start=str(Event_Start)       
        if(len(Event_Start)!=10):
            Event_Start=np.nan
                
        Event_End = Lease_data['enddate'][i]
            
        #Depth
        Depth = -Lease_data['fracture_md'][i]
              
        #Strike
        Strike = Lease_data['azimuth'][i]
        
        #Dip
        if(str(Lease_data['dip_magnitude'][i])=="nan"):
            Dip=-1
        else:
            Dip = Lease_data['dip_magnitude'][i]
    
        #Est. Event Diameter
        if(str(Lease_data['frac_diameter'][i])=="nan"):
            Diameter = 250
        else:
            Diameter = Lease_data['frac_diameter'][i]
            
        #NAD27
        Easting27 = Lease_data['x_nad27'][i]
        Northing27 = Lease_data['y_nad27'][i]
        
        #check source candidate list
        if source_query['Source Well'][source_query['EventDetailsID']==Lease_data['EventDetailsID'][i]][source_query['Source Well'][source_query['EventDetailsID']==Lease_data['EventDetailsID'][i]].index[0]]==-1:
            
            #SourceWell
            if comment=="NaN":
                Source="NaN"   
            k=0
            sources=[]
            while k < len(allwells):
                if ((str(' '+allwells['WELL_NAME'][k].lower()+' ') in comment.lower()) or (str(' '+allwells['REG_NAME'][k]+' ') in comment.lower()) 
                    or (str(' ' + allwells['ALIAS'][k]+ ' ') in comment.lower()) or (str('-' + allwells['ALIAS2'][k]+' ') in comment.lower())):
                    sources.append(allwells['WELL_NAME'][k])
                k=k+1
        
            if len(sources)>0:
                sources=set(sources)
                sources=list(sources)
                Source=sources
            else:
                try:
                    NearWell=comment.split("by well ",1)[1].split(" and ",1)[0]
                    #if(NearWell[0:7]=="South C"):
                    #    NearWell=NearWell
                    if(len(NearWell)>17):
                        NearWell=NearWell.split(".",1)[0]
                        if(len(NearWell)>17):                    
                            NearWell=NearWell.split(" was ",1)[0]
                            if(len(NearWell)>17): 
                                NearWell=NearWell.split(" but ",1)[0]
                                if(len(NearWell)>17):
                                    NearWell=NearWell.split(",",1)[0]
                except:
                    try:
                        NearWell=comment.split(" wells ",1)[1].split(" and ",1)[0]
                        if(NearWell[0:7]=="South C"):
                            NearWell=NearWell
                        elif(len(NearWell)>12):
                            NearWell=NearWell.split(", ",1)[0]
                        SecondWell=comment.split(" wells ",1)[1].split("and ",1)[1].split(".",1)[0]
                        if(len(NearWell)>17):
                            NearWell=comment.split(" wells ",1)[1].split(".",1)[0]
                    except:
                        NearWell=comment
                #if(NearWell[0:7]=="South C"):
                #        NearWell=NearWell
                if(len(NearWell)>17):
                    try:
                        NearWell=comment.split(" well ",1)[1].split(" and ",1)[0]
                        if(len(NearWell)>17):
                            NearWell=comment.split(" well ",1)[1].split(" was ",1)[0]
                            if(NearWell[0:7]=="South C"):
                                NearWell=NearWell
                            elif(len(NearWell)>17):
                                try:
                                    NearWell=comment.split(" well ",1)[1].split(" but ",1)[0]
                                except:
                                    NearWell=comment.split(" well ",1)[1].split(" came ",1)[0]
                                if(len(NearWell)>17):
                                    NearWell=comment.split(" well ",1)[1].split(".",1)[0]
                                    if(len(NearWell)>17):
                                        try:
                                            NearWell=comment.split(" well ",1)[1].split(" ad ",1)[0]
                                        except:
                                            NearWell=comment
                        if(len(NearWell)>17):
                            NearWell=comment.split(" wells ",1)[1].split(" and ",1)[0]
                            if(len(NearWell)>15):
                                NearWell=NearWell.split(",",1)[0]
                    except:
                        NearWell=comment
                if(NearWell[0:7]=="South C"):
                    NearWell=NearWell
                elif(NearWell[0:2]=="for"):
                    NearWell=comment.split("for ",1)[1].split(" and",1)[0]
                elif(len(NearWell)>14):
                    try:
                        NearWell=comment.split("for ",1)[1].split(" and",1)[0]
                        if(len(NearWell)>17):
                            try:
                                NearWell=comment.split(" wells ",1)[1].split(" and ",1)[0]
                            except:
                                NearWell=comment.split(" for ",1)[1].split(",",1)[0]
                                if(len(NearWell)>17):
                                    NearWell=comment.split(" for ",1)[1].split(".",1)[0]
                    except:
                        NearWell=comment
                #if(NearWell[0:7]=="South C"):
                #        NearWell=NearWell        
                if(len(NearWell)>17):
                    NearWell="NaN"
                if(NearWell=='this well'):
                    NearWell="NaN"
                k=0
                while k < len(allwells):
                    if ((str(allwells['WELL_NAME'][k].lower()) == NearWell.lower()) or 
                        (str(allwells['REG_NAME'][k].lower()) == NearWell.lower()) or 
                        (str(allwells['ALIAS'][k].lower()) == NearWell.lower()) or 
                        (str(allwells['ALIAS2'][k].lower()) == NearWell.lower())):
                        NearWell=allwells['WELL_NAME'][k]
                    k=k+1
        
        #     #SourceWell
                Source = NearWell
                Source=str(Source)
        #     if(Source[0:4]=="19Z "):
        #         Source=Source.replace(" ","-")
        else:   
            Source=source_query['Source Well'][source_query['EventDetailsID']==Lease_data['EventDetailsID'][i]][source_query['Source Well'][source_query['EventDetailsID']==Lease_data['EventDetailsID'][i]].index[0]]
        #get top perf, asset, field, lease, spud date, x, ys
        if(Source=="NaN"):
            tp=np.nan
            asset=np.nan
            lease=np.nan
            field=np.nan
            drillyr=np.nan
            xsurf=np.nan
            ysurf=np.nan
            xbh=np.nan
            ybh=np.nan
        else:
            if len(Source[0])==1:
                Source=Source
            else:
                Source=Source[0]
            k=0
            while k <len(wellbore_df):        
                if(wellbore_df['REG_NAME'][k].lower()==Source.lower()):
                    tp=-wellbore_df['TopPerf'][k]
                    asset=wellbore_df['ASSET'][k]
                    lease=wellbore_df['FIELD'][k]
                    field=wellbore_df['LEASE'][k]
                    drillyr=wellbore_df['DRILL_YEAR'][k]
                    xsurf=wellbore_df['XCOORD_SURF'][k]
                    ysurf=wellbore_df['YCOORD_SURF'][k]
                    xbh=wellbore_df['XCOORD_BH'][k]
                    ybh=wellbore_df['YCOORD_BH'][k]
                    k=len(wellbore_df)+1
                elif(wellbore_df['WELL_NAME'][k].lower()==Source[0].lower()):
                    tp=-wellbore_df['TopPerf'][k]
                    asset=wellbore_df['ASSET'][k]
                    lease=wellbore_df['FIELD'][k]
                    field=wellbore_df['LEASE'][k]
                    drillyr=wellbore_df['DRILL_YEAR'][k]
                    xsurf=wellbore_df['XCOORD_SURF'][k]
                    ysurf=wellbore_df['YCOORD_SURF'][k]
                    xbh=wellbore_df['XCOORD_BH'][k]
                    ybh=wellbore_df['YCOORD_BH'][k]
                    k=len(wellbore_df)+1
                else:
                    k=k+1        
            if(k==len(wellbore_df)):
                tp=np.nan
                asset=np.nan
                lease=np.nan
                field=np.nan
                drillyr=np.nan
                xsurf=np.nan
                ysurf=np.nan
                xbh=np.nan
                ybh=np.nan
            
        #add event to dataframe
        Leaseevent_df = Leaseevent_df.append({'Event Start': Event_Start,'Event End': Event_End,'Depth': Depth,'Strike Azimuth': Strike,'Dip': Dip,'Estimated Event Diameter': Diameter,'NAD27 Easting': Easting27,'NAD27 Northing': Northing27,'Source Well': Source,'Top Perf':tp,'Asset':asset,'Field':field,'Lease':lease,'Drill Year':drillyr,'X_Surf':xsurf,'Y_Surf':ysurf,'X_BH':xbh,'Y_BH':ybh,'TOD':TOD},ignore_index = True)
        
        i = i+1
        
    Leaseevent_df['Event Start']=pd.to_datetime(Leaseevent_df['Event Start'])
    Leaseevent_df['Event End']=pd.to_datetime(Leaseevent_df['Event End'])
    
   # Leaseevent_df['Estimated Event Diameter'].mean()
   # Leaseevent_df=Leaseevent_df[Leaseevent_df['Event End']>pd.to_datetime('1/1/2017')]
    #Leaseevent_df['Estimated Event Diameter'].mean()/2
    #Leaseevent_df['Estimated Event Diameter'].mean()/2
    
    # In[199]:
    
    
    #create equations of a circle for each seep
    Seep_df=pd.DataFrame(columns=['Name','X','Y','Z','Xcir','Ycir','Zcir'])
    
    if Asset=='KKSCW':
        path=r'\\fs01.sentinelpeakresources.local\I Drive\Assets\SJV\Frac_Model_HTML\Additional Layers\KKSCW Seeps and Lease Lines.xlsx'
    if Asset=='MCK':
        path=r'\\fs01.sentinelpeakresources.local\I Drive\Assets\SJV\Frac_Model_HTML\Additional Layers\MCK Seeps and Lease Lines.xlsx'
    if Asset=='EMRMZ':
        path=r'\\fs01.sentinelpeakresources.local\I Drive\Assets\SJV\Frac_Model_HTML\Additional Layers\EMRMZ Seeps and Lease Lines.xlsx'    
    
    Seeps=pd.read_excel(path,sheet_name='SEEPS')    
    name=Seeps['Name']
    x=Seeps['X']
    y=Seeps['Y']
    z=Seeps['Z']
        
    theta = np.linspace(0, 2*np.pi, 45)
    i=0
    while i < len(name):   
        strike = 0
        dip = 0 
    
        cx = x[i] # Seep easting
        cy = y[i] # Seep northing
        cz = z[i] #surface
        r=100 #seep radius
    
        #equations of a circle
    
        axx=cx+r*np.cos(np.pi/2-strike)
        ay=cy+r*np.sin(np.pi/2-strike)
        az=0#cz 
    
        j =r*np.sin(np.pi/2-dip)
        bangle = strike
    
        bx=cx-j*np.cos(bangle)
        by=cy+j*np.sin(bangle)
        bz=0#cz+r*np.cos(np.pi/2-dip)
    
        acx=axx-cx
        acy=ay-cy
        acz=az-cz
        bcx=bx-cx
        bcy=by-cy
        bcz=bz-cz
    
        maga=(acx**2+acy**2+acz**2)**0.5
        magb=(bcx**2+bcy**2+bcz**2)**0.5
    
        #generate 3d coordinates for each frac from equations of circle
        x1=cx+r*(np.cos(theta)*acx/maga+np.sin(theta)*bcx/magb)
        y1=cy+r*(np.cos(theta)*acy/maga+np.sin(theta)*bcy/magb)
        z1=cz+r*(np.cos(theta)*acz/maga+np.sin(theta)*bcz/magb)
    
        data={'Name':name[i],'X':x[i],'Y':y[i],'Z':z[i],'Xcir':x1,'Ycir':y1,'Zcir':z1}
        Seep_df=Seep_df.append(pd.Series(data,index=Seep_df.columns),ignore_index=True)
        i=i+1
    
    
    # In[200]:
    
    
    #create equations for lease lines
    Leaseline_df=pd.DataFrame(columns=['Side','X','Y','Z'])
    
    if Asset=='KKSCW':
        path=r'\\fs01.sentinelpeakresources.local\I Drive\Assets\SJV\Frac_Model_HTML\Additional Layers\KKSCW Seeps and Lease Lines.xlsx'
    if Asset=='MCK':
        path=r'\\fs01.sentinelpeakresources.local\I Drive\Assets\SJV\Frac_Model_HTML\Additional Layers\MCK Seeps and Lease Lines.xlsx'
    if Asset=='EMRMZ':
        path=r'\\fs01.sentinelpeakresources.local\I Drive\Assets\SJV\Frac_Model_HTML\Additional Layers\EMRMZ Seeps and Lease Lines.xlsx'
    
    Leaselines=pd.read_excel(path,sheet_name='Lease Line')
    i=0
    while i < len(Leaselines):
        if i == len(Leaselines)-1:
           m=(Leaselines['Y'][0]-Leaselines['Y'][i])/(Leaselines['X'][0]-Leaselines['X'][i])
           b=Leaselines['Y'][0]-m*Leaselines['X'][0]
           x=np.linspace(Leaselines['X'][0],Leaselines['X'][i],50)
        else:
            m=(Leaselines['Y'][i+1]-Leaselines['Y'][i])/(Leaselines['X'][i+1]-Leaselines['X'][i])
            b=Leaselines['Y'][i+1]-m*Leaselines['X'][i+1]
            x=np.linspace(Leaselines['X'][i+1],Leaselines['X'][i],50)
        y=m*x+b
        z=np.linspace(-0.5,-0.5,50)
        Leaseline_df=Leaseline_df.append({'Side':Leaselines['Corner'][i],'X':x,'Y':y,'Z':z},ignore_index=True)
        i=i+1
        
    #NEX=Leaselines['X'][Leaselines['Corner']=='NE'].values
    #SEX=Leaselines['X'][Leaselines['Corner']=='SE'].values
    #NEY=Leaselines['Y'][Leaselines['Corner']=='NE'].values
    #SEY=Leaselines['Y'][Leaselines['Corner']=='SE'].values
    #NWX=Leaselines['X'][Leaselines['Corner']=='NW'].values
    #SWX=Leaselines['X'][Leaselines['Corner']=='SW'].values
    #NWY=Leaselines['Y'][Leaselines['Corner']=='NW'].values
    #SWY=Leaselines['Y'][Leaselines['Corner']=='SW'].values
    #
    #m_e=(NEY-SEY)/(NEX-SEX)
    #m_n=(NEY-NWY)/(NEX-SWX)
    #m_w=(NWY-SWY)/(NWX-SWX)
    #m_s=(SEY-SWY)/(SEX-SWX)
    #b_e=NEY-m_e*NEX
    #b_n=NEY-m_n*NEX
    #b_w=NWY-m_w*NWX
    #b_s=SEY-m_s*SEX
    #xs_e=np.linspace(NEX,SEX,50)
    #x_e=[]
    #i=0
    #while i < 50:
    #    x_e.append(xs_e[i][0])
    #    i=i+1
    #xs_n=np.linspace(NEX,SWX,50)
    #x_n=[]
    #i=0
    #while i < 50:
    #    x_n.append(xs_n[i][0])
    #    i=i+1
    #xs_w=np.linspace(NWX,SWX,50)
    #x_w=[]
    #i=0
    #while i < 50:
    #    x_w.append(xs_w[i][0])
    #    i=i+1
    #xs_s=np.linspace(SEX,SWX,50)
    #x_s=[]
    #i=0
    #while i < 50:
    #    x_s.append(xs_s[i][0])
    #    i=i+1
    #ys_e=m_e*x_e+b_e
    #ys_n=m_n*x_n+b_n
    #ys_w=m_w*x_w+b_w
    #ys_s=m_s*x_s+b_s
    #zs=np.linspace(-0.5,-0.5,50)
    #Leaseline_df=Leaseline_df.append({'Side':'East Leaseline','X':x_e,'Y':ys_e,'Z':zs},ignore_index=True)
    #Leaseline_df=Leaseline_df.append({'Side':'North Leaseline','X':x_n,'Y':ys_n,'Z':zs},ignore_index=True)
    #Leaseline_df=Leaseline_df.append({'Side':'West Leaseline','X':x_w,'Y':ys_w,'Z':zs},ignore_index=True)
    #Leaseline_df=Leaseline_df.append({'Side':'South Leaseline','X':x_s,'Y':ys_s,'Z':zs},ignore_index=True)
    
    
    # In[201]:
    
    
    if Asset =='KKSCW':
        KKSCWZone1_1=pd.read_excel(path3,sheet_name='1-1')
        KKSCWZone2_1=pd.read_excel(path3,sheet_name='2-1')
        KKSCWZone3_1=pd.read_excel(path3,sheet_name='3-1')
        KKSCWZone4_1=pd.read_excel(path3,sheet_name='4-1')
        KKSCWZone5_1=pd.read_excel(path3,sheet_name='5-1')
        KKSCWZone6_1=pd.read_excel(path3,sheet_name='6-1')
        KKSCWZone7_1=pd.read_excel(path3,sheet_name='7-1')
        KKSCWZoneG_1=pd.read_excel(path3,sheet_name='G-1')
        KKSCWZoneOCT=pd.read_excel(path3,sheet_name='OPAL CT')
        KKSCWZoneRF=pd.read_excel(path3,sheet_name='REVERSE FAULT 1')
        KKSCWTOD_df=pd.read_excel(path3,sheet_name='TOD')
        KKSCWZone1_1['Z[MD]']=-KKSCWZone1_1['Z[MD]']
        KKSCWZone2_1['Z[MD]']=-KKSCWZone2_1['Z[MD]']
        KKSCWZone3_1['Z[MD]']=-KKSCWZone3_1['Z[MD]']
        KKSCWZone4_1['Z[MD]']=-KKSCWZone4_1['Z[MD]']
        KKSCWZone5_1['Z[MD]']=-KKSCWZone5_1['Z[MD]']
        KKSCWZone6_1['Z[MD]']=-KKSCWZone6_1['Z[MD]']
        KKSCWZone7_1['Z[MD]']=-KKSCWZone7_1['Z[MD]']
        KKSCWZoneG_1['Z[MD]']=-KKSCWZoneG_1['Z[MD]']
        KKSCWZoneOCT['Z[MD]']=-KKSCWZoneOCT['Z[MD]']
        KKSCWZoneRF['Z[MD]']=-KKSCWZoneRF['Z[MD]']
        KKSCWTOD_df['Z[MD]']=-KKSCWTOD_df['Z[MD]']
    if Asset =='MCK':
        #MCKSurf=pd.read_excel(path3,sheet_name='Ground Surface')
        MCKBaseD=pd.read_excel(path3,sheet_name='Base Diatomite 50x50')
        MCKTopD=pd.read_excel(path3,sheet_name='Top Diatomite 50x50')
        MCKBaseD=MCKBaseD[['X','Y','Z[MD]']]
        MCKTopD=MCKTopD[['X','Y','Z[MD]']]
        #MCKSurf['Depth']=-MCKSurf['Depth']
        MCKBaseD['Z[MD]']=-MCKBaseD['Z[MD]']
        MCKTopD['Z[MD]']=-MCKTopD['Z[MD]']
    if Asset =='EMRMZ':
         EMRMZTopD=pd.read_excel(path3,sheet_name='TOD')
         EMRMZTopD['Z[MD]']=-EMRMZTopD['Z[MD]']
    
    
    # In[202]:
    
    
    #generate random color list for color correlation
    
    colors='''
            aliceblue, antiquewhite, aqua, aquamarine, azure,
            beige, bisque, black, blanchedalmond, blue,
            blueviolet, brown, burlywood, cadetblue,
            chartreuse, chocolate, coral, cornflowerblue,
            cornsilk, crimson, cyan, darkblue, darkcyan,
            darkgoldenrod, darkgray, darkgrey, darkgreen,
            darkkhaki, darkmagenta, darkolivegreen, darkorange,
            darkorchid, darkred, darksalmon, darkseagreen,
            darkslateblue, darkslategray, darkslategrey,
            darkturquoise, darkviolet, deeppink, deepskyblue,
            dimgray, dimgrey, dodgerblue, firebrick,
            floralwhite, forestgreen, fuchsia, gainsboro,
            ghostwhite, gold, goldenrod, gray, grey, green,
            greenyellow, honeydew, hotpink, indianred, indigo,
            ivory, khaki, lavender, lavenderblush, lawngreen,
            lemonchiffon, lightblue, lightcoral, lightcyan,
            lightgoldenrodyellow, lightgray, lightgrey,
            lightgreen, lightpink, lightsalmon, lightseagreen,
            lightskyblue, lightslategray, lightslategrey,
            lightsteelblue, lightyellow, lime, limegreen,
            linen, magenta, maroon, mediumaquamarine,
            mediumblue, mediumorchid, mediumpurple,
            mediumseagreen, mediumslateblue, mediumspringgreen,
            mediumturquoise, mediumvioletred, midnightblue,
            mintcream, mistyrose, moccasin, navajowhite, navy,
            oldlace, olive, olivedrab, orange, orangered,
            orchid, palegoldenrod, palegreen, paleturquoise,
            palevioletred, papayawhip, peachpuff, peru, pink,
            plum, powderblue, purple, red, rosybrown,
            royalblue, saddlebrown, salmon, sandybrown,
            seagreen, seashell, sienna, silver, skyblue,
            slateblue, slategray, slategrey, snow, springgreen,
            steelblue, tan, teal, thistle, tomato, turquoise,
            violet, wheat, white, whitesmoke, yellow,
            yellowgreen
            '''
    colorlist=colors.split(',')
    colorlist=[l.replace('\n','') for l in colorlist]
    colorlist=[l.replace(' ','') for l in colorlist]
    #if(len(colorlist)-len(wellbore_df)>0): 
    #    randomlist=random.sample(range(0,len(colorlist)),len(colorlist)-len(wellbore_df))
    #    randomlist.sort()
    #    randomlist=list(set(randomlist))
    #    colorlistnew=np.delete(colorlist,randomlist).tolist()
    #else:
    #    colorlistnew=colorlist
        
    #####
    #wellbore_df['Colors']=colorlistnew
    
    
    # In[203]:
    
    
    #create equations of a circle for each frac
    
    LeaseFrac_eqs=pd.DataFrame(columns=['Depth','Radius','Easting','Northing','ACX','ACY','ACZ','BCX','BCY','BCZ','MAGA','MAGB','Dip','Strike','Event Start','Event End','Source Well','Top Perf','Asset','Field','Lease','Drill Year','X_Surf','Y_Surf','X_BH','Y_BH','TOD'])
    
    #DepthReference = 'Middle'#'Middle' #'Error Bottom' 'Error Top'
    
    theta = np.linspace(0, 2* np.pi, 90)
    i=0
    
    while i < len(Leaseevent_df.index):
        event_start= Leaseevent_df['Event Start'][i]
        event_end = Leaseevent_df['Event End'][i]
        source_well = Leaseevent_df['Source Well'][i]
        dip=Leaseevent_df['Dip'][i]
        
        strike = Leaseevent_df['Strike Azimuth'][i]/360*2*np.pi #convert to radians
        if(Leaseevent_df['Dip'][i]==-1):
            dip=-1
        else:
            dip = Leaseevent_df['Dip'][i]/360*2*np.pi #convert to radians   
        cx = Leaseevent_df['NAD27 Easting'][i] # event easting
        cy = Leaseevent_df['NAD27 Northing'][i] # event northing
        tp=Leaseevent_df['Top Perf'][i]
        asset=Leaseevent_df['Asset'][i]
        lease=Leaseevent_df['Lease'][i]
        field=Leaseevent_df['Field'][i]
        drillyr=Leaseevent_df['Drill Year'][i]
        xsurf=Leaseevent_df['X_Surf'][i]
        ysurf=Leaseevent_df['Y_Surf'][i]
        xbh=Leaseevent_df['X_BH'][i]
        ybh=Leaseevent_df['Y_BH'][i]
        TOD=Leaseevent_df['TOD'][i]
        #if DepthReference == 'Error Top':
        #    cz = -df['Error Bound Top'][i] # event depth taken as error bound top
        #elif DepthReference == 'Error Bottom':
        #    cz = -df['Error Bound Bottom'][i] # event depth taken as error bound bottom
        #else:
        cz = Leaseevent_df['Depth'][i] # event depth
        
        r=Leaseevent_df['Estimated Event Diameter'][i]/2 #event radius
    
        #equations of a circle
    
        #a vector equation changes in each quadrant
        if (0<=strike<np.pi/2):
            axx=cx+r*np.cos(np.pi/2-strike)
            ay=cy+r*np.sin(np.pi/2-strike)
        elif (np.pi/2<=strike<np.pi):
            axx=cx+r*np.cos(strike-np.pi/2)
            ay=cy-r*np.sin(strike-np.pi/2)
        elif (np.pi<=strike<3*np.pi/2):
            axx=cx-r*np.cos(3*np.pi/2-strike)
            ay=cy-r*np.sin(3*np.pi/2-strike)
        else:
            axx=cx-r*np.cos(strike-3*np.pi/2)
            ay=cy+r*np.sin(strike-3*np.pi/2)    
    
        az=cz 
    
        j =r*np.sin(np.pi/2-dip)
    
        #bangle changes in each quadrant
        if (0<=strike<=np.pi/2):
            bangle = strike
        elif (np.pi/2<strike<np.pi):
            bangle = np.pi-strike
        elif (np.pi<=strike<=3*np.pi/2):
            bangle = strike-np.pi
        else:
            bangle = 2*np.pi-strike
    
        #b vector changes in each quadrant
        if (0<=strike<=np.pi/2):
            bx=cx-j*np.cos(bangle)
            by=cy+j*np.sin(bangle)
        elif (np.pi/2<strike<np.pi):
            bx=cx+j*np.cos(bangle)
            by=cy+j*np.sin(bangle)
        elif (np.pi<=strike<=3*np.pi/2):
            bx=cx+j*np.cos(bangle)
            by=cy-j*np.sin(bangle)
        else:
            bx=cx-j*np.cos(bangle)
            by=cy-j*np.sin(bangle) 
    
        bz=cz+r*np.cos(np.pi/2-dip)
    
        acx=axx-cx
        acy=ay-cy
        acz=az-cz
        bcx=bx-cx
        bcy=by-cy
        bcz=bz-cz
    
        maga=(acx**2+acy**2+acz**2)**0.5
        magb=(bcx**2+bcy**2+bcz**2)**0.5
    
        #dcx=acy/maga*bcz-acz/maga*bcy
        #dcy=acz/maga*bcx-acx/maga*bcz
        #dcz=acx/maga*bcy-acy/maga*bcx
    
        #magd=(dcx**2+dcy**2+dcz**2)**0.5
        strike=Leaseevent_df['Strike Azimuth'][i]
        LeaseFrac_eqs=LeaseFrac_eqs.append(pd.Series([cz,r,cx,cy,acx,acy,acz,bcx,bcy,bcz,maga,magb,dip,strike,event_start,event_end,source_well,tp,asset,field,lease,drillyr,xsurf,ysurf,xbh,ybh,TOD],index=LeaseFrac_eqs.columns),ignore_index=True)
        i=i+1
    
    
    # In[204]:
    
    
    #generate 3d coordinates for each frac from equations of circle
    
    #Frac_eqs = pd.merge(Frac_eqs,Perf_df,left_on=['Source Well'], right_on = ['Source Well'], how = 'left')
    LeasePosition_df=pd.DataFrame(columns=['X','Y','Z','Event Start','Event End','Source Well','Top Perf','Dip','Strike','Asset','Field','Lease','Drill Year','X_Surf','Y_Surf','X_BH','Y_BH','Radius','TOD'])#,'Colors'])
    i=0
    while i < len(LeaseFrac_eqs.index):
        x1=LeaseFrac_eqs['Easting'][i]+LeaseFrac_eqs['Radius'][i]*(np.cos(theta)*LeaseFrac_eqs['ACX'][i]/LeaseFrac_eqs['MAGA'][i]+np.sin(theta)*LeaseFrac_eqs['BCX'][i]/LeaseFrac_eqs['MAGB'][i])
        y1=LeaseFrac_eqs['Northing'][i]+LeaseFrac_eqs['Radius'][i]*(np.cos(theta)*LeaseFrac_eqs['ACY'][i]/LeaseFrac_eqs['MAGA'][i]+np.sin(theta)*LeaseFrac_eqs['BCY'][i]/LeaseFrac_eqs['MAGB'][i])
        z1=LeaseFrac_eqs['Depth'][i]+LeaseFrac_eqs['Radius'][i]*(np.cos(theta)*LeaseFrac_eqs['ACZ'][i]/LeaseFrac_eqs['MAGA'][i]+np.sin(theta)*LeaseFrac_eqs['BCZ'][i]/LeaseFrac_eqs['MAGB'][i])
        t1=LeaseFrac_eqs['Event Start'][i]
        t2=LeaseFrac_eqs['Event End'][i]
        tp=LeaseFrac_eqs['Top Perf'][i]
        x1=np.append(x1,np.array([LeaseFrac_eqs['Easting'][i]]),axis=0)
        y1=np.append(y1,np.array([LeaseFrac_eqs['Northing'][i]]),axis=0)
        z1=np.append(z1,np.array([LeaseFrac_eqs['Depth'][i]]),axis=0)
        if(LeaseFrac_eqs['Dip'][i]==-1):
            dip=-1
        else:
            dip=LeaseFrac_eqs['Dip'][i]*180/np.pi
        strike=LeaseFrac_eqs['Strike'][i]
        asset=LeaseFrac_eqs['Asset'][i]
        lease=LeaseFrac_eqs['Lease'][i]
        field=LeaseFrac_eqs['Field'][i]
        drillyr=LeaseFrac_eqs['Drill Year'][i]
        xsurf=LeaseFrac_eqs['X_Surf'][i]
        ysurf=LeaseFrac_eqs['Y_Surf'][i]
        xbh=LeaseFrac_eqs['X_BH'][i]
        ybh=LeaseFrac_eqs['Y_BH'][i]
        source_well=LeaseFrac_eqs['Source Well'][i]
        radius=LeaseFrac_eqs['Radius'][i]
        TOD=LeaseFrac_eqs['TOD'][i]
        #colors=Frac_eqs['Colors'][i]
        data={'X':x1,'Y':y1,'Z':z1,'Event Start':t1,'Event End':t2,'Source Well':source_well,'Top Perf':tp,'Dip':dip,'Strike':strike,'Asset':asset,'Field':field,'Lease':lease,'Drill Year':drillyr,'X_Surf':xsurf,'Y_Surf':ysurf,'X_BH':xbh,'Y_BH':ybh,'Radius':radius,'TOD':TOD}#,'Colors':colors}
        LeasePosition_df=LeasePosition_df.append(data,ignore_index=True)
        i=i+1
    
    LeasePosition_df=LeasePosition_df[LeasePosition_df['Dip']>=0]
    LeasePosition_df=LeasePosition_df.reset_index()
    LeasePosition_df=LeasePosition_df.sort_values('index')
    LeasePosition_df=LeasePosition_df.drop(['index'],axis=1)
    LeasePosition_df['Event Start']=pd.to_datetime(LeasePosition_df['Event Start'])
    
    LeasePosition_df['day']=LeasePosition_df['Event Start'].dt.day
    LeasePosition_df['month']=LeasePosition_df['Event Start'].dt.month
    LeasePosition_df['year']=LeasePosition_df['Event Start'].dt.year   
    LeasePosition_df['day end']=LeasePosition_df['Event End'].dt.day
    LeasePosition_df['month end']=LeasePosition_df['Event End'].dt.month
    LeasePosition_df['year end']=LeasePosition_df['Event End'].dt.year
    LeasePosition_df['year end']=LeasePosition_df['year end'].astype(float)
    
    
    # In[205]:
    
    #Create Summary Table
    LeaseFracCharacteristic_df=pd.DataFrame(columns=['Xmin','Xmax','Ymin','Ymax','Zavg','Source Well','BHX','BHY','Top Perf','Dip','Strike','Year End','TOD','Radius'])
    
    i=0
    count=len(LeasePosition_df)
    while i < count:
        xmin = LeasePosition_df['X'][i].min()
        xmax = LeasePosition_df['X'][i].max()
        ymin = LeasePosition_df['Y'][i].min()
        ymax = LeasePosition_df['Y'][i].max()
        z=LeasePosition_df['Z'][i].mean()
        source=LeasePosition_df['Source Well'][i]
        bhx=LeasePosition_df['X_BH'][i]
        bhy=LeasePosition_df['Y_BH'][i]
        tp=LeasePosition_df['Top Perf'][i]
        dip=LeasePosition_df['Dip'][i]
        strike=LeasePosition_df['Strike'][i]
        yearend=LeasePosition_df['year end'][i]
        TOD=LeasePosition_df['TOD'][i]
        radius=LeasePosition_df['Radius'][i]
        data = {'Xmin':xmin,'Xmax':xmax,'Ymin':ymin,'Ymax':ymax,'Zavg':z,'Source Well':source,'BHX':bhx,'BHY':bhy,'Top Perf':tp,'Dip':dip,'Strike':strike,'Year End':yearend,'TOD':TOD,'Radius':radius}
        LeaseFracCharacteristic_df=LeaseFracCharacteristic_df.append(data,ignore_index=True)
        i=i+1

    LeaseSummary_df=Leasewellbore_df.copy()
    LeaseSummary_df=LeaseSummary_df.drop(['wellzonenum'],axis=1)
    LeaseSummary_df=LeaseSummary_df.drop(['API_No'],axis=1)
    LeaseSummary_df=LeaseSummary_df.drop(['ALIAS'],axis=1)
    LeaseSummary_df=LeaseSummary_df.drop(['XCOORD_COMP'],axis=1)
    LeaseSummary_df=LeaseSummary_df.drop(['YCOORD_COMP'],axis=1)
    LeaseSummary_df=LeaseSummary_df.drop(['LATNAD83'],axis=1)
    LeaseSummary_df=LeaseSummary_df.drop(['LONGNAD83'],axis=1)
    LeaseSummary_df=LeaseSummary_df.drop(['WELL_SYMBOL'],axis=1)
    LeaseSummary_df=LeaseSummary_df.drop(['COMPL_YEAR'],axis=1)
    LeaseSummary_df.drop_duplicates(inplace=True)
    LeaseSummary_df.reset_index(inplace=True)
    LeaseSummary_df=LeaseSummary_df.drop(['index'],axis=1)
    
    LeaseSummary_df['Event Count']=0
    LeaseSummary_df['Avg Event Depth']=np.nan
    LeaseSummary_df['Avg Event Radius']=np.nan
    LeaseSummary_df['Avg Dip of Events']=np.nan
    LeaseSummary_df['Avg Strike of Events']=np.nan
    LeaseSummary_df['Avg Event Distance from Source']=np.nan
    LeaseSummary_df['Disorder Value']=np.nan
    LeaseSummary_df['Avg Depth Diff btw Successive Events']=np.nan
    LeaseSummary_df['Intersection Count']=np.nan
    LeaseSummary_df['Intersection Count After Spud']=np.nan
    LeaseSummary_df['Intersection from Source Count']=np.nan
    LeaseSummary_df['Avg Intersection Depth']=np.nan
    LeaseSummary_df['Avg Intersection After Spud Depth']=np.nan
    LeaseSummary_df['Avg Dip of Intersecting Events']=np.nan
    LeaseSummary_df['Intersection Wells']=np.nan
    LeaseSummary_df['Intersecting Disorder Value']=np.nan
    LeaseSummary_df['Avg Depth Diff btw Successive Intersecting Events']=np.nan
    LeaseSummary_df=LeaseSummary_df.astype(object)
    
    i=0
    while i <len(LeaseSummary_df):
        if(str(LeaseSummary_df['XCOORD_BH'][i])=="nan"):
            LeaseSummary_df['XCOORD_BH'][i]=LeaseSummary_df['XCOORD_SURF'][i]
            LeaseSummary_df['YCOORD_BH'][i]=LeaseSummary_df['YCOORD_SURF'][i]
        i=i+1
        
    i=0
    k=0
    eventcount=0
    sourcecount=0
    eventafterspud=0
    interdepths=[]
    eventdepths=[]
    wells=[]
    dips=[]
    afterspuddepths=[]
    
    while i < len(LeaseSummary_df):
        while k <len(LeaseFracCharacteristic_df):
            #find intersecting fracs for given well
            if (LeaseFracCharacteristic_df['Xmin'][k]<=LeaseSummary_df['XCOORD_BH'][i] 
                and LeaseFracCharacteristic_df['Xmax'][k]>=LeaseSummary_df['XCOORD_BH'][i]
                and LeaseFracCharacteristic_df['Ymin'][k]<=LeaseSummary_df['YCOORD_BH'][i] 
                and LeaseFracCharacteristic_df['Ymax'][k]>=LeaseSummary_df['YCOORD_BH'][i]
                #and FracCharacteristic_df['Zavg'][k]>=Summary_df['TopPerf'][i]
               ):
                    #count the fracs and record the depths, source well names, and dips
                    eventcount=eventcount+1
                    if(LeaseSummary_df['DRILL_YEAR'][i]<=LeaseFracCharacteristic_df['Year End'][k]):
                        eventafterspud=eventafterspud+1
                        afterspuddepths.append(LeaseFracCharacteristic_df['Zavg'][k])
                    interdepths.append(LeaseFracCharacteristic_df['Zavg'][k])
                    wells.append(LeaseFracCharacteristic_df['Source Well'][k])
                    dips.append(LeaseFracCharacteristic_df['Dip'][k])
                    if (LeaseFracCharacteristic_df['Source Well'][k].lower()==(LeaseSummary_df['WELL_NAME'][i].lower() or LeaseSummary_df['REG_NAME'][i].lower())):
                        sourcecount=sourcecount+1          
    
            k=k+1
        #assign the values to the summary table
        LeaseSummary_df['Intersection Count'][i]=eventcount
        LeaseSummary_df['Intersection Count After Spud'][i]=eventafterspud
        LeaseSummary_df['Intersection from Source Count'][i]=sourcecount
        if eventcount == 0:
            LeaseSummary_df['Avg Intersection Depth'][i]=np.nan
            LeaseSummary_df['Avg Intersection After Spud Depth'][i]=np.nan
            LeaseSummary_df['Avg Dip of Intersecting Events'][i]=np.nan
        else:
            #take the average dip and depth
            LeaseSummary_df['Avg Intersection Depth'][i]=np.array(interdepths).mean()
            LeaseSummary_df['Avg Intersection After Spud Depth'][i]=np.array(afterspuddepths).mean()
            LeaseSummary_df['Avg Dip of Intersecting Events'][i]=np.array(dips).mean()
                
        LeaseSummary_df['Intersection Wells'][i]=np.array(wells)
        #reset counters
        eventcount=0
        sourcecount=0
        eventafterspud=0
        wells=[]
        afterspuddepths=[]
        dips=[]
        #calculate disorder from intersecting fracs
        if len(interdepths)==0:
            disorder=np.nan
            avgdiffintersource=np.nan
        elif len(interdepths)==1:
            disorder=np.nan
            avgdiffintersource=np.nan
        else:
            indices = list(range(len(interdepths)))
            indices.sort(key=lambda x: interdepths[x])
            output = [0] * len(indices)
            for j, x in enumerate(indices):
                output[x] = j
    
            length=len(interdepths)
            order= list(range(0,length))
            difference = []
    
            zip_object = zip(output, order)
            for output_j, order_j in zip_object:
                difference.append(output_j-order_j)
    
            absdifference =list(map(abs,difference))
            disorder= sum(absdifference)/length 
            
            #calculate average difference between each successive frac for the given source well intersecting fracs
            diff_list = [] 
            for x, y in zip(np.array(interdepths[0::]), np.array(interdepths[1::])): 
                diff_list.append(y-x)
            avgdiffintersource=np.array(diff_list).mean()
            
        LeaseSummary_df['Avg Depth Diff btw Successive Intersecting Events'][i]=avgdiffintersource
        LeaseSummary_df['Intersecting Disorder Value'][i]=disorder
        interdepths=[]
        disorder=0
        avgdiffintersource=0
        i=i+1
        k=0
    
    i=0
    k=0
    orderofdepths=[]
    orderofradii=[]
    dips=[]
    strikes=[]
    distance=[]
    #get chronological order of fracs
    while i < len(LeaseSummary_df):
        while k < len(LeaseFracCharacteristic_df):
            if (LeaseFracCharacteristic_df['Source Well'][k].lower()==(LeaseSummary_df['WELL_NAME'][i].lower() or LeaseSummary_df['REG_NAME'][i].lower())):
                orderofdepths.append([LeaseFracCharacteristic_df['Zavg'][k]])
                orderofradii.append([LeaseFracCharacteristic_df['Radius'][k]])
                dips.append(LeaseFracCharacteristic_df['Dip'][k])
                strikes.append(LeaseFracCharacteristic_df['Strike'][k])
                distance.append(((LeasePosition_df['X_BH'][k]-LeasePosition_df['X'][k][-1])**2+(LeasePosition_df['Y_BH'][k]-LeasePosition_df['Y'][k][-1])**2)**0.5)
            k=k+1
            
        if len(orderofdepths)==1:
            disorder=np.nan
            LeaseSummary_df['Event Count'][i]=1
            LeaseSummary_df['Avg Event Depth'][i]=np.array(orderofdepths).mean()
            LeaseSummary_df['Avg Event Radius'][i]=np.array(orderofradii).mean()
            LeaseSummary_df['Avg Dip of Events'][i]=np.array(dips).mean()
            LeaseSummary_df['Avg Strike of Events'][i]=np.array(strikes).mean()
            LeaseSummary_df['Avg Event Distance from Source'][i]=np.array(distance).mean()
            avgdiffsource=np.nan
        else:    
            LeaseSummary_df['Avg Event Depth'][i]=np.array(orderofdepths).mean()
            LeaseSummary_df['Avg Event Radius'][i]=np.array(orderofradii).mean()
            LeaseSummary_df['Avg Dip of Events'][i]=np.array(dips).mean()
            LeaseSummary_df['Avg Strike of Events'][i]=np.array(strikes).mean()
            LeaseSummary_df['Avg Event Distance from Source'][i]=np.array(distance).mean()
            #calculate disorder value for events
            indices = list(range(len(orderofdepths)))
            indices.sort(key=lambda x: orderofdepths[x])
            output = [0] * len(indices)
            for j, x in enumerate(indices):
                output[x] = j
    
            length=len(orderofdepths)
            LeaseSummary_df['Event Count'][i]=length
            order= list(range(0,length))
            difference = []
    
            zip_object = zip(output, order)
            for output_j, order_j in zip_object:
                difference.append(output_j-order_j)
    
            absdifference =list(map(abs,difference))
            try:
                disorder= sum(absdifference)/length 
            except:
                disorder=np.nan # if 0 events
                
            #calculate average difference between each successive frac for the given source well
            diff_list = [] 
            for x, y in zip(np.array(orderofdepths[0::]), np.array(orderofdepths[1::])): 
                diff_list.append(y-x)
            avgdiffsource=np.array(diff_list).mean()
        
        #assign values    
        LeaseSummary_df['Avg Depth Diff btw Successive Events'][i]=avgdiffsource
        LeaseSummary_df['Disorder Value'][i]=disorder
        #reset counters
        k=0
        disorder=0
        avgdiffsource=0
        orderofdepths=[]
        dips=[]
        strikes=[]
        distance=[]
        i=i+1     

    LeaseSummary_df=LeaseSummary_df.drop(['REG_NAME'],axis=1)
    LeaseSummary_df=LeaseSummary_df.drop(['XCOORD_SURF'],axis=1)
    LeaseSummary_df=LeaseSummary_df.drop(['YCOORD_SURF'],axis=1)
    LeaseSummary_df=LeaseSummary_df.drop(['XCOORD_BH'],axis=1)
    LeaseSummary_df=LeaseSummary_df.drop(['YCOORD_BH'],axis=1)
    LeaseSummary_df=LeaseSummary_df.drop(['GROUND_ELEV'],axis=1)
    LeaseSummary_df=LeaseSummary_df.drop(['TVD'],axis=1)
    LeaseSummary_df=LeaseSummary_df.drop(['ASSET'],axis=1)
    LeaseSummary_df=LeaseSummary_df.drop(['FIELD'],axis=1)
    # In[206]:
    
    if Asset == 'KKSCW':
        LeaseSummary_df.sort_values(['Event Count']).to_excel(r'\\fs01.sentinelpeakresources.local\I Drive\Assets\Midway Sunset Belridge\Staff Folders\Joseph Kenrick\Well Health\Event Data\KKSCW Summary Event Data Table.xlsx')
    if Asset == 'EMRMZ':
        LeaseSummary_df.sort_values(['Event Count']).to_excel(r'\\fs01.sentinelpeakresources.local\I Drive\Assets\Midway Sunset Belridge\Staff Folders\Joseph Kenrick\Well Health\Event Data\EMRMZ Summary Event Data Table.xlsx')
    if Asset == 'MCK':
        LeaseSummary_df.sort_values(['Event Count']).to_excel(r'\\fs01.sentinelpeakresources.local\I Drive\Assets\Midway Sunset Belridge\Staff Folders\Joseph Kenrick\Well Health\Event Data\MCK Summary Event Data Table.xlsx')
    
    # In[207]:
    
    
    #Plot all events within given radius of given well
    j=0
    while j < len(welllist):
        Radius=200 #feet
        Well = welllist['WELL_NAME'][j]
        Year=2018
    
        x1=wellbore_df['XCOORD_SURF'][wellbore_df['WELL_NAME']==Well].iloc[0]
        y1=wellbore_df['YCOORD_SURF'][wellbore_df['WELL_NAME']==Well].iloc[0]
        if(wellbore_df['XCOORD_BH'][wellbore_df['WELL_NAME']==Well].iloc[0]==-1):
            x2=x1
            y2=y1
        else:
            x2=wellbore_df['XCOORD_BH'][wellbore_df['WELL_NAME']==Well].iloc[0]
            y2=wellbore_df['YCOORD_BH'][wellbore_df['WELL_NAME']==Well].iloc[0]
            
        z=wellbore_df['TVD'][wellbore_df['WELL_NAME']==Well].iloc[0]
        z=-z
        xmin=x2-Radius
        xmax=x2+Radius
        ymin=y2-Radius
        ymax=y2+Radius
    
        #get perfs within radius
        PerfData=wellbore_df[['WELL_NAME','TVD','XCOORD_SURF','YCOORD_SURF','XCOORD_BH','YCOORD_BH','DRILL_YEAR','ABAND_YEAR','ZONE']].copy()   
        i=0
        while i < len(wellbore_df):
            if(wellbore_df['XCOORD_BH'][i]==-1):
                xcoord=wellbore_df['XCOORD_SURF'][i]
                ycoord=wellbore_df['YCOORD_SURF'][i]
            else:
                xcoord=wellbore_df['XCOORD_BH'][i]
                ycoord=wellbore_df['YCOORD_BH'][i]
                
            if(xcoord>xmin and xcoord<xmax
              and ycoord>ymin and ycoord<ymax):
                i=i+1
            else:
                PerfData=PerfData.drop(i) 
                i=i+1
        
        PerfData=PerfData.drop_duplicates()
        if Asset=='MCK':
            PerfData=PerfData[PerfData['ZONE']=='DIATOMITE']
        #PerfData['ABAND_YEAR']=PerfData['ABAND_YEAR'].replace('N/A',9999)
        #PerfData['ABAND_YEAR']=PerfData['ABAND_YEAR'].astype('float')
        #PerfData=PerfData[PerfData['ABAND_YEAR']>=Year]
        #PerfData['ABAND_YEAR']=PerfData['ABAND_YEAR'].astype('int')
        #PerfData['ABAND_YEAR']=PerfData['ABAND_YEAR'].replace(9999,'N/A')
        PerfData.reset_index(inplace=True)
        PerfData=PerfData.drop(['index'],axis=1)
        PerfData['TopPerf']=np.nan
        i=0
        while i <len(PerfData):
            PerfData['TopPerf'][i]=wellbore_df['TopPerf'][wellbore_df['WELL_NAME']==PerfData['WELL_NAME'][i]].max()
            if(PerfData['XCOORD_BH'][i]==-1):
                PerfData['XCOORD_BH'][i]=PerfData['XCOORD_SURF'][i]
                PerfData['YCOORD_BH'][i]=PerfData['YCOORD_SURF'][i]
            i=i+1
        
        i=0
        PerfData['Colors']='rgb(20,20,20)'
        while i < len(PerfData):
            if(PerfData['WELL_NAME'][i]==Well):
                PerfData['Colors'][i]='rgb(120,220,120)'
            i=i+1
    
        #get events within radius
        WellData=LeasePosition_df.copy()
        i=0
        while i < len(LeasePosition_df):
            if(LeasePosition_df['X'][i].mean()>xmin and LeasePosition_df['X'][i].mean()<xmax
              and LeasePosition_df['Y'][i].mean()>ymin and LeasePosition_df['Y'][i].mean()<ymax):
                i=i+1
            else:
                WellData=WellData.drop(i) 
                i=i+1
    
        WellData=WellData[WellData['year end']>Year]
        if(len(WellData)==0):
            j=j+1
        else:
            WellData.reset_index(inplace=True)
            WellData['Colors']=np.nan
            
            #get first source well for color matching
            WellData['Source Well 2']=np.nan
            #i=0
            #while i < len(WellData):
            #    WellData['Source Well 2'][i]=str(WellData['Source Well'][i][0])
            #    if (len(str(WellData['Source Well 2'][i]))==1):
            WellData['Source Well 2']=WellData['Source Well']
            #    i=i+1
    
            #find min and max X and Y for TOD grid
            if Asset=='KKSCW':
                #Get TOD over range
                WellTOD=KKSCWTOD_df[KKSCWTOD_df['X']>(xmin-50)].copy()
                WellTOD=WellTOD[WellTOD['X']<(xmax+50)]
                WellTOD=WellTOD[WellTOD['Y']>(ymin-50)]
                WellTOD=WellTOD[WellTOD['Y']<(ymax+50)]
                WellTOD.reset_index(inplace=True)
                AvgTOD=WellTOD['Z[MD]'].mean()
    
                #Get 7-1 over range
                Well7_1=KKSCWZone7_1[KKSCWZone7_1['X']>(xmin-50)].copy()
                Well7_1=Well7_1[Well7_1['X']<(xmax+50)]
                Well7_1=Well7_1[Well7_1['Y']>(ymin-50)]
                Well7_1=Well7_1[Well7_1['Y']<(ymax+50)]
                Well7_1.reset_index(inplace=True)
    
                #Get RF over range
                WellRF=KKSCWZoneRF[KKSCWZoneRF['X']>(xmin-50)].copy()
                WellRF=WellRF[WellRF['X']<(xmax+50)]
                WellRF=WellRF[WellRF['Y']>(ymin-50)]
                WellRF=WellRF[WellRF['Y']<(ymax+50)]
                WellRF.reset_index(inplace=True)
    
                #Get OCT over range
                WellOCT=KKSCWZoneOCT[KKSCWZoneOCT['X']>(xmin-50)].copy()
                WellOCT=WellOCT[WellOCT['X']<(xmax+50)]
                WellOCT=WellOCT[WellOCT['Y']>(ymin-50)]
                WellOCT=WellOCT[WellOCT['Y']<(ymax+50)]
                WellOCT.reset_index(inplace=True)
    
                #Get 4-1 over range
                Well4_1=KKSCWZone4_1[KKSCWZone4_1['X']>(xmin-50)].copy()
                Well4_1=Well4_1[Well4_1['X']<(xmax+50)]
                Well4_1=Well4_1[Well4_1['Y']>(ymin-50)]
                Well4_1=Well4_1[Well4_1['Y']<(ymax+50)]
                Well4_1.reset_index(inplace=True)
    
                #Get 2-1 over range
                Well2_1=KKSCWZone2_1[KKSCWZone2_1['X']>(xmin-50)].copy()
                Well2_1=Well2_1[Well2_1['X']<(xmax+50)]
                Well2_1=Well2_1[Well2_1['Y']>(ymin-50)]
                Well2_1=Well2_1[Well2_1['Y']<(ymax+50)]
                Well2_1.reset_index(inplace=True)
    
                #Get 1-1 over range
                Well1_1=KKSCWZone1_1[KKSCWZone1_1['X']>(xmin-50)].copy()
                Well1_1=Well1_1[Well1_1['X']<(xmax+50)]
                Well1_1=Well1_1[Well1_1['Y']>(ymin-50)]
                Well1_1=Well1_1[Well1_1['Y']<(ymax+50)]
                Well1_1.reset_index(inplace=True)
    
                #Get 3-1 over range
                Well3_1=KKSCWZone3_1[KKSCWZone3_1['X']>(xmin-50)].copy()
                Well3_1=Well3_1[Well3_1['X']<(xmax+50)]
                Well3_1=Well3_1[Well3_1['Y']>(ymin-50)]
                Well3_1=Well3_1[Well3_1['Y']<(ymax+50)]
                Well3_1.reset_index(inplace=True)
    
                #Get 5-1 over range
                Well5_1=KKSCWZone5_1[KKSCWZone5_1['X']>(xmin-50)].copy()
                Well5_1=Well5_1[Well5_1['X']<(xmax+50)]
                Well5_1=Well5_1[Well5_1['Y']>(ymin-50)]
                Well5_1=Well5_1[Well5_1['Y']<(ymax+50)]
                Well5_1.reset_index(inplace=True)
    
                #Get 6-1 over range
                Well6_1=KKSCWZone6_1[KKSCWZone6_1['X']>(xmin-50)].copy()
                Well6_1=Well6_1[Well6_1['X']<(xmax+50)]
                Well6_1=Well6_1[Well6_1['Y']>(ymin-50)]
                Well6_1=Well6_1[Well6_1['Y']<(ymax+50)]
                Well6_1.reset_index(inplace=True)
    
                #Get G-1 over range
                WellG_1=KKSCWZoneG_1[KKSCWZoneG_1['X']>(xmin-50)].copy()
                WellG_1=WellG_1[WellG_1['X']<(xmax+50)]
                WellG_1=WellG_1[WellG_1['Y']>(ymin-50)]
                WellG_1=WellG_1[WellG_1['Y']<(ymax+50)]
                WellG_1.reset_index(inplace=True)
                
            if Asset =='MCK':           
                #base diatomite
                Wellbased=MCKBaseD[MCKBaseD['X']>(xmin-50)].copy()
                Wellbased=Wellbased[Wellbased['X']<(xmax+50)]
                Wellbased=Wellbased[Wellbased['Y']>(ymin-50)]
                Wellbased=Wellbased[Wellbased['Y']<(ymax+50)]
                Wellbased.reset_index(inplace=True)
                
                #top diatomite
                Welltopd=MCKTopD[MCKTopD['X']>(xmin-50)].copy()
                Welltopd=Welltopd[Welltopd['X']<(xmax+50)]
                Welltopd=Welltopd[Welltopd['Y']>(ymin-50)]
                Welltopd=Welltopd[Welltopd['Y']<(ymax+50)]
                Welltopd.reset_index(inplace=True)
                AvgTOD=Welltopd['Z[MD]'].mean()
                
            if Asset =='EMRMZ':                      
                #top diatomite
                Welltopd=EMRMZTopD[EMRMZTopD['X']>(xmin-50)].copy()
                Welltopd=Welltopd[Welltopd['X']<(xmax+50)]
                Welltopd=Welltopd[Welltopd['Y']>(ymin-50)]
                Welltopd=Welltopd[Welltopd['Y']<(ymax+50)]
                Welltopd.reset_index(inplace=True)
                AvgTOD=Welltopd['Z[MD]'].mean()
                
            #Only get seeps in view
            i=0
            WellSeeps=Seep_df.copy()
            while i < len(Seep_df):
                if(Seep_df['X'][i]>xmin-50 and Seep_df['X'][i]<xmax+50
                  and Seep_df['Y'][i]>ymin-50 and Seep_df['Y'][i]<ymax+50):
                    i=i+1
                else:
                    WellSeeps=WellSeeps.drop(i) 
                    i=i+1 
            WellSeeps.reset_index(inplace=True)
            
            #get lease lines in view
            i=0
                   
            #generate color list
            colors8=px.colors.sequential.Blues
            colors2=px.colors.sequential.Greens
            colors3=px.colors.sequential.Reds
            colors4=px.colors.sequential.Purples
            colors=px.colors.sequential.speed
            colors6=px.colors.sequential.Plotly3
            colors7=px.colors.qualitative.Prism
            colors5=px.colors.sequential.Plasma_r
    
            colorscale = colors5+colors7+colorlist+colors6+colors3+colors4+colors2+colors8+colors
            i=0
            k=0
            while k < WellData['Source Well 2'].nunique():
                while i < len(WellData):    
                    if(WellData['Source Well 2'][i]==WellData['Source Well 2'].value_counts().index[k]):
                        WellData['Colors'][i]=colorscale[k]
                    i=i+1
                k=k+1
                i=0
    
            WellData['TOD']=WellData['TOD'].astype('Int32')
            WellData=WellData.sort_values('Event End',ascending=True)
            WellData.reset_index(inplace=True)
            #WellData.reset_index(inplace=True)
            WellData=WellData.drop(['level_0'],axis=1)
            WellData=WellData.drop(['index'],axis=1)
    
            #grab events only from well in question
            SourceWellEvents=WellData[WellData['Source Well 2']==Well].copy()
            indices=SourceWellEvents.index
            
            ### plot by radius around Well
    
            layout=go.Layout(margin={'l': 0, 'r': 0, 'b': 0, 't': 0})
            data=[]
            #add north arrow first
            #data.append(go.Scatter3d(x=[xmin,xmin],y=[ymin+80,ymin],z=[0,0],mode='lines',name="North Arrow",visible=True,line=dict(color='rgba(0, 0, 0, 0.5)',width=20)))
            data.append(go.Cone(x=[xmin-60],y=[ymin-60],z=[0],u=[0],v=[60],w=[40],showscale=False,colorscale=[[0, 'rgb(0,0,0)'], [1, 'rgb(0,0,0)']],name='North Arrow',
                                text='North Arrow'))
            if Asset=='KKSCW':
                #plot TOD
                data.append(go.Scatter3d(x=WellTOD['X'],y=WellTOD['Y'],z=WellTOD['Z[MD]'],mode='markers',opacity=0.4,name='TOD',marker=dict(
                            color='rgba(135, 10, 250, 0.5)',size=3,line=dict(color='MediumPurple',width=0)),visible=True))
                fig_network = go.Figure(data=data, layout=layout)
                #plot 1-1
                data.append(go.Scatter3d(x=Well1_1['X'],y=Well1_1['Y'],z=Well1_1['Z[MD]'],mode='markers',opacity=0.2,name='1-1',marker=dict(
                            color='rgba(235, 206, 50, 0.5)',size=3,line=dict(color='MediumPurple',width=0)),visible='legendonly'))
                #plot 2-1
                data.append(go.Scatter3d(x=Well2_1['X'],y=Well2_1['Y'],z=Well2_1['Z[MD]'],mode='markers',opacity=0.3,name='2-1',marker=dict(
                            color='rgba(20, 124, 33, 0.5)',size=3,line=dict(color='MediumPurple',width=0)),visible='legendonly'))
                #plot 3-1
                data.append(go.Scatter3d(x=Well3_1['X'],y=Well3_1['Y'],z=Well3_1['Z[MD]'],mode='markers',opacity=0.2,name='3-1',marker=dict(
                            color='rgba(105, 206, 250, 0.5)',size=3,line=dict(color='MediumPurple',width=0)),visible='legendonly'))
                #plot 4-1
                data.append(go.Scatter3d(x=Well4_1['X'],y=Well4_1['Y'],z=Well4_1['Z[MD]'],mode='markers',opacity=0.4,name='4-1',marker=dict(
                            color='rgba(10, 100, 100, 0.5)',size=3,line=dict(color='MediumPurple',width=0)),visible='legendonly'))
                #plot 5-1
                data.append(go.Scatter3d(x=Well5_1['X'],y=Well5_1['Y'],z=Well5_1['Z[MD]'],mode='markers',opacity=0.2,name='5-1',marker=dict(
                            color='rgba(200, 205, 230, 0.5)',size=3,line=dict(color='MediumPurple',width=0)),visible='legendonly'))
                #plot 6-1
                data.append(go.Scatter3d(x=Well6_1['X'],y=Well6_1['Y'],z=Well6_1['Z[MD]'],mode='markers',opacity=0.2,name='6-1',marker=dict(
                            color='rgba(85, 206, 112, 0.5)',size=3,line=dict(color='MediumPurple',width=0)),visible='legendonly'))
                #plot 7-1
                data.append(go.Scatter3d(x=Well7_1['X'],y=Well7_1['Y'],z=Well7_1['Z[MD]'],mode='markers',opacity=0.2,name='7-1',marker=dict(
                            color='rgba(135, 206, 10, 0.5)',size=3,line=dict(color='MediumPurple',width=0)),visible='legendonly'))
                #plot G-1
                data.append(go.Scatter3d(x=WellG_1['X'],y=WellG_1['Y'],z=WellG_1['Z[MD]'],mode='markers',opacity=0.2,name='G-1',marker=dict(
                            color='rgba(135, 135, 135, 0.5)',size=3,line=dict(color='MediumPurple',width=0)),visible='legendonly'))
                #plot OCT
                data.append(go.Scatter3d(x=WellOCT['X'],y=WellOCT['Y'],z=WellOCT['Z[MD]'],mode='markers',opacity=0.2,name='Opal CT',marker=dict(
                            color='rgba(15, 15, 15, 0.5)',size=3,line=dict(color='MediumPurple',width=0)),visible='legendonly'))
                #plot RF
                data.append(go.Scatter3d(x=WellRF['X'],y=WellRF['Y'],z=WellRF['Z[MD]'],mode='markers',opacity=0.2,name='Reverse Fault',marker=dict(
                            color='rgba(250, 10, 10, 0.5)',size=3,line=dict(color='MediumPurple',width=0)),visible='legendonly'))
                geolayers=12
                
            if Asset=='MCK':
                #plot TopD
                data.append(go.Scatter3d(x=Welltopd['X'],y=Welltopd['Y'],z=Welltopd['Z[MD]'],mode='markers',opacity=0.9,name='Top Diatomite',marker=dict(
                            color='rgba(135, 10, 250, 0.5)',size=5,line=dict(color='MediumPurple',width=0)),visible=True))
                #plot BaseD
                data.append(go.Scatter3d(x=Wellbased['X'],y=Wellbased['Y'],z=Wellbased['Z[MD]'],mode='markers',opacity=0.9,name='Base Diatomite',marker=dict(
                            color='rgba(35, 206, 50, 0.5)',size=5,line=dict(color='MediumPurple',width=0)),visible=True))
                geolayers=3
                
            if Asset=='EMRMZ':
                #plot TopD
                data.append(go.Scatter3d(x=Welltopd['X'],y=Welltopd['Y'],z=Welltopd['Z[MD]'],mode='markers',opacity=0.9,name='Top Diatomite',marker=dict(
                            color='rgba(135, 10, 250, 0.5)',size=5,line=dict(color='MediumPurple',width=0)),visible=True))
    #            #plot BaseD
    #            data.append(go.Scatter3d(x=Wellbased['X'],y=Wellbased['Y'],z=Wellbased['Z[MD]'],mode='markers',opacity=0.9,name='Base Diatomite',marker=dict(
    #                        color='rgba(35, 206, 50, 0.5)',size=3,line=dict(color='MediumPurple',width=0)),visible=True))
                geolayers=2
                
            #plot wellbores and perfs
            k=0
            while k <len(PerfData):
                #plot wellbore
                x=[PerfData['XCOORD_SURF'][k],PerfData['XCOORD_BH'][k]]
                y=[PerfData['YCOORD_SURF'][k],PerfData['YCOORD_BH'][k]]
                z=[0,-PerfData['TVD'][k]]
                data.append(go.Scatter3d(x=x,y=y,z=z,text=str(PerfData['WELL_NAME'][k])+
                                         str(' | Top Perf:')+str(PerfData['TopPerf'][k])+'<br>'+
                                         str(' | DRL:')+str(PerfData['DRILL_YEAR'][k])+
                                         str(' | ABN:')+str(PerfData['ABAND_YEAR'][k]),
                                         mode='lines',name=PerfData['WELL_NAME'][k],line=dict(color=PerfData['Colors'][k],width=20),visible=True))
                #calculate x/y of top perf
                xtp1=(-PerfData['TopPerf'][k]+PerfData['TVD'][k]*PerfData['XCOORD_SURF'][k]/(PerfData['XCOORD_SURF'][k]-PerfData['XCOORD_BH'][k]))/(PerfData['TVD'][k]/(PerfData['XCOORD_SURF'][k]-PerfData['XCOORD_BH'][k]))
                xtp2=(-PerfData['TopPerf'][k]-30+PerfData['TVD'][k]*PerfData['XCOORD_SURF'][k]/(PerfData['XCOORD_SURF'][k]-PerfData['XCOORD_BH'][k]))/(PerfData['TVD'][k]/(PerfData['XCOORD_SURF'][k]-PerfData['XCOORD_BH'][k]))
                
                ytp1=(-PerfData['TopPerf'][k]+PerfData['TVD'][k]*PerfData['YCOORD_SURF'][k]/(PerfData['YCOORD_SURF'][k]-PerfData['YCOORD_BH'][k]))/(PerfData['TVD'][k]/(PerfData['YCOORD_SURF'][k]-PerfData['YCOORD_BH'][k]))
                ytp2=(-PerfData['TopPerf'][k]-30+PerfData['TVD'][k]*PerfData['YCOORD_SURF'][k]/(PerfData['YCOORD_SURF'][k]-PerfData['YCOORD_BH'][k]))/(PerfData['TVD'][k]/(PerfData['YCOORD_SURF'][k]-PerfData['YCOORD_BH'][k]))
                
                #plot top perf
                x=[xtp2,xtp1]
                y=[ytp2,ytp1]
                z=[-PerfData['TopPerf'][k]-30,-PerfData['TopPerf'][k]]
                data.append(go.Scatter3d(x=x,y=y,z=z,text=str(PerfData['WELL_NAME'][k])+' Top Perf',mode='lines',name=PerfData['WELL_NAME'][k],
                                         line=dict(color='rgba(250, 250, 250, 0.5)',width=25),visible=True))
                
                tickdepth=95
                while tickdepth < 1000:
                #calculate x/y of wellbore rulers               
                    xtick_1=(-tickdepth+PerfData['TVD'][k]*PerfData['XCOORD_SURF'][k]/(PerfData['XCOORD_SURF'][k]-PerfData['XCOORD_BH'][k]))/(PerfData['TVD'][k]/(PerfData['XCOORD_SURF'][k]-PerfData['XCOORD_BH'][k]))
                    xtick_2=(-tickdepth-10+PerfData['TVD'][k]*PerfData['XCOORD_SURF'][k]/(PerfData['XCOORD_SURF'][k]-PerfData['XCOORD_BH'][k]))/(PerfData['TVD'][k]/(PerfData['XCOORD_SURF'][k]-PerfData['XCOORD_BH'][k]))
    
                    ytick_1=(-tickdepth+PerfData['TVD'][k]*PerfData['YCOORD_SURF'][k]/(PerfData['YCOORD_SURF'][k]-PerfData['YCOORD_BH'][k]))/(PerfData['TVD'][k]/(PerfData['YCOORD_SURF'][k]-PerfData['YCOORD_BH'][k]))
                    ytick_2=(-tickdepth-10+PerfData['TVD'][k]*PerfData['YCOORD_SURF'][k]/(PerfData['YCOORD_SURF'][k]-PerfData['YCOORD_BH'][k]))/(PerfData['TVD'][k]/(PerfData['YCOORD_SURF'][k]-PerfData['YCOORD_BH'][k]))
    
                    #plot wellbore rulers
                    x=[xtick_2,xtick_1]
                    y=[ytick_2,ytick_1]
                    z=[-tickdepth-10,-tickdepth]
                    data.append(go.Scatter3d(x=x,y=y,z=z,text=str(tickdepth+5),mode='lines',
                                             name=str(tickdepth+5)+'ft',line=dict(color='rgba(250, 50, 50, 0.5)',width=20),visible=True))
                    tickdepth=tickdepth+100
                k=k+1
    
            #plot Seeps
            i=0
            while i < len(WellSeeps):
                data.append(go.Scatter3d(x=WellSeeps['Xcir'][i],y=WellSeeps['Ycir'][i],z=WellSeeps['Zcir'][i],text=WellSeeps['Name'][i],
                                         name=WellSeeps['Name'][i],surfaceaxis=1,surfacecolor='rgba(250, 250, 250, 0.5)',
                                         mode='lines',line=dict(width=10,color='rgba(250, 250, 250, 0.5)'),visible=True))
                i=i+1
            
            #plot leaselines
            i=0
            while i < len(Leaseline_df):
                data.append(go.Scatter3d(x=Leaseline_df['X'][i],y=Leaseline_df['Y'][i],z=Leaseline_df['Z'][i],
                                        name=Leaseline_df['Side'][i],text=Leaseline_df['Side'][i],
                                        mode='lines',line=dict(width=20,color='rgba(50,50,50,0.5)'),visible=True))
                i=i+1
                
            #group and plot fracs
            traces=[]
            i=0
            while i < len(WellData):
                traces.append(go.Scatter3d(x=WellData['X'][i],y=WellData['Y'][i],z=WellData['Z'][i],
                                                   text=str(WellData['Source Well'][i])+str(' | ')
                                                       +str(WellData['Event End'][i])
                                                       +'<br>'+'Event Radius='+str(WellData['Radius'][i]),
                                                   name=str(WellData['Source Well 2'][i])+'|'
                                                       +str(WellData['Event End'][i].date()),
                                                   surfaceaxis=1,surfacecolor=WellData['Colors'][i],
                                                   mode='lines',line=dict(color=WellData['Colors'][i])))
                i=i+1   
    
            grouped_traces= []
            dateranges=[]
            groupedeventdata=[]
            groupedeventTOD=[]
            
            dateranges.append(str(WellData['Event End'].min().date())+' to '+str(WellData['Event End'].max().date()))
            groupedeventdata.append(int(WellData['Z'].mean().mean()))
            try:
                groupedeventTOD.append(int(WellData['TOD'].mean()))
            except:
                groupedeventTOD.append((WellData['TOD'].mean()))
            
            i=0
            while i < len(traces):
                grouped_traces.append(traces[i:i+6])
                dateranges.append(str(WellData['Event End'][i:i+6].min().date())+' to '+str(WellData['Event End'][i:i+6].max().date()))
                groupedeventdata.append(int(WellData['Z'][i:i+6].mean().mean()))
                try:
                    groupedeventTOD.append(int(WellData['TOD'][i:i+6].mean()))
                except:
                    groupedeventTOD.append((WellData['TOD'][i:i+6].mean()))
                i=i+6
            if len(SourceWellEvents)>0:
                dateranges.append(Well)
                groupedeventdata.append(int(SourceWellEvents['Z'].mean().mean()))
                try:
                    groupedeventTOD.append(int(SourceWellEvents['TOD'].mean()))
                except:
                    groupedeventTOD.append((SourceWellEvents['TOD'].mean()))
                
            for idx,item in enumerate(grouped_traces):
                data.extend(grouped_traces[idx])
    
            fig_network = go.Figure(data=data, layout=layout)
            steps = []
            step=[]
                   
            stepcount=0
            #first step, all events on
            step=dict(method = 'update',args=[{'visible': [False] * len(fig_network.data)},
                                                  {'title.text':dateranges[stepcount],
                                                  'annotations[0].text':'Avg Depth of Events in Step:' + str(groupedeventdata[stepcount])+
                                                  '<br>'+'Avg TOD of Events in Step:' + str(groupedeventTOD[stepcount])}
                                                  ])
            k=2
            while k <len(fig_network.data):
                #keep diatomite layers as they were
                step['args'][0]['visible'][0]=True
                fig_network.data[0]['showlegend']=True
                step['args'][0]['visible'][1]=True
                fig_network.data[1]['showlegend']=True
                while k < geolayers:
                    step['args'][0]['visible'][k]='legendonly'
                    fig_network.data[k]['showlegend']=True
                    k+=1
                #turn everything else on
                step['args'][0]['visible'][k] = True 
                fig_network.data[k]['showlegend']=True
                k+=1
    
            steps.append(step)
            stepcount+=1
    
            i=len(PerfData)*12+len(WellSeeps)+geolayers+len(Leaseline_df)
            while i < len(fig_network.data):
                step=dict(method = 'update',args=[{'visible': [False] * len(fig_network.data)},
                                                  {'title.text':dateranges[stepcount],
                                                  'annotations[0].text':'Avg Depth of Events in Step:' + str(groupedeventdata[stepcount])+
                                                  '<br>'+'Avg TOD of Events in Step:' + str(groupedeventTOD[stepcount])}
                                                  ])
    
                #keep diatomite layers as they were
                step['args'][0]['visible'][0]=True
                fig_network.data[0]['showlegend']=True
                step['args'][0]['visible'][1]=True
                fig_network.data[1]['showlegend']=True
                k=2
                #set starting visibility for geolayers
                while k < geolayers:
                    step['args'][0]['visible'][k]='legendonly' 
                    fig_network.data[k]['showlegend']=True
                    k+=1
                #keep all wellbores, top perfs, and wellbore ticks visible, but only wellbores in legend
                while k < geolayers+len(PerfData)*12:
                    step['args'][0]['visible'][k]=True
                    fig_network.data[k]['showlegend']=True
                    step['args'][0]['visible'][k+1]=True
                    fig_network.data[k+1]['showlegend']=False
                    step['args'][0]['visible'][k+2]=True
                    fig_network.data[k+2]['showlegend']=False
                    step['args'][0]['visible'][k+3]=True
                    fig_network.data[k+3]['showlegend']=False
                    step['args'][0]['visible'][k+4]=True
                    fig_network.data[k+4]['showlegend']=False
                    step['args'][0]['visible'][k+5]=True
                    fig_network.data[k+5]['showlegend']=False
                    step['args'][0]['visible'][k+6]=True
                    fig_network.data[k+6]['showlegend']=False
                    step['args'][0]['visible'][k+7]=True
                    fig_network.data[k+7]['showlegend']=False
                    step['args'][0]['visible'][k+8]=True
                    fig_network.data[k+8]['showlegend']=False
                    step['args'][0]['visible'][k+9]=True
                    fig_network.data[k+9]['showlegend']=False
                    step['args'][0]['visible'][k+10]=True
                    fig_network.data[k+10]['showlegend']=False
                    step['args'][0]['visible'][k+11]=True
                    fig_network.data[k+11]['showlegend']=False
                    k+=12
                #make seeps and leaselines visible
                while k < len(PerfData)*12+len(WellSeeps)+geolayers+len(Leaseline_df):
                    step['args'][0]['visible'][k]=True
                    fig_network.data[k]['showlegend']=True
                    k+=1
    
                #toggle the group on for each step
                step['args'][0]['visible'][i] = True 
                fig_network.data[i]['showlegend']=True
                i+=1
                if i < len(fig_network.data):
                    step['args'][0]['visible'][i] = True
                    fig_network.data[i]['showlegend']=True
                    i+=1
                if i < len(fig_network.data):
                    step['args'][0]['visible'][i] = True
                    fig_network.data[i]['showlegend']=True
                    i+=1
                if i < len(fig_network.data):
                    step['args'][0]['visible'][i] = True
                    fig_network.data[i]['showlegend']=True
                    i+=1
                if i < len(fig_network.data):
                    step['args'][0]['visible'][i] = True
                    fig_network.data[i]['showlegend']=True
                    i+=1
                if i < len(fig_network.data):
                    step['args'][0]['visible'][i] = True
                    fig_network.data[i]['showlegend']=True
                    i+=1
                stepcount+=1
    
                steps.append(step)
            
            if len(SourceWellEvents)>0:
                step=dict(method = 'update',args=[{'visible': [False] * len(fig_network.data)},
                                                  {'title.text':dateranges[stepcount],
                                                  'annotations[0].text':'Avg Depth of Events in Step:' + str(groupedeventdata[stepcount])+
                                                  '<br>'+'Avg TOD of Events in Step:' + str(groupedeventTOD[stepcount])}
                                                  ])
    
                #keep diatomite layers as they were
                step['args'][0]['visible'][0]=True
                fig_network.data[0]['showlegend']=True
                step['args'][0]['visible'][1]=True
                fig_network.data[1]['showlegend']=True
                k=2
                #set starting visibility for geolayers
                while k < geolayers:
                    step['args'][0]['visible'][k]='legendonly' 
                    fig_network.data[k]['showlegend']=True
                    k+=1
                #keep all wellbores and top perfs visible, but only wellbores in legend
                while k < geolayers+len(PerfData)*12:
                    step['args'][0]['visible'][k]=True
                    fig_network.data[k]['showlegend']=True
                    step['args'][0]['visible'][k+1]=True
                    fig_network.data[k+1]['showlegend']=False
                    step['args'][0]['visible'][k+2]=True
                    fig_network.data[k+2]['showlegend']=False
                    step['args'][0]['visible'][k+3]=True
                    fig_network.data[k+3]['showlegend']=False
                    step['args'][0]['visible'][k+4]=True
                    fig_network.data[k+4]['showlegend']=False
                    step['args'][0]['visible'][k+5]=True
                    fig_network.data[k+5]['showlegend']=False
                    step['args'][0]['visible'][k+6]=True
                    fig_network.data[k+6]['showlegend']=False
                    step['args'][0]['visible'][k+7]=True
                    fig_network.data[k+7]['showlegend']=False
                    step['args'][0]['visible'][k+8]=True
                    fig_network.data[k+8]['showlegend']=False
                    step['args'][0]['visible'][k+9]=True
                    fig_network.data[k+9]['showlegend']=False
                    step['args'][0]['visible'][k+10]=True
                    fig_network.data[k+10]['showlegend']=False
                    step['args'][0]['visible'][k+11]=True
                    fig_network.data[k+11]['showlegend']=False
                    k+=12
                #make seeps and leaselines visible
                while k < len(PerfData)*12+len(WellSeeps)+geolayers+len(Leaseline_df):
                    step['args'][0]['visible'][k]=True
                    fig_network.data[k]['showlegend']=True
                    k+=1
                i=0
                while i <len(SourceWellEvents):
                    step['args'][0]['visible'][indices[i]+k]=True
                    fig_network.data[indices[i]+k]['showlegend']=True
                    i=i+1
                stepcount+=1
                steps.append(step)
                        
            sliders = [dict(active=0, steps=steps)]
                                                  
            fig_network.update_layout(sliders=sliders,title={'text':dateranges[0],'xref':'paper','yref':'paper','x':0,'y':.97},
                                      annotations=[dict(text=steps[0]['args'][1]['annotations[0].text'],
                                                xref='paper',yref='paper',x=1,y=0.97,align='right',showarrow=False,visible=True,
                                                bordercolor='black',borderwidth=1)])
            fig_network['layout']['sliders'][0]['pad']['t']=0
    
            #get view bounds
            i=0
            xs=[]
            ys=[]
            zs=[]
            while i <len(WellData):
                xs=np.concatenate([xs,WellData['X'][i]])
                ys=np.concatenate([ys,WellData['Y'][i]])
                zs=np.concatenate([zs,WellData['Z'][i]])
                i=i+1
    
            fig_network.update_layout(scene = dict(
                xaxis = dict(nticks=10, range=[xs.min()-20,xs.max()+20],),
                yaxis = dict(nticks=10, range=[ys.min()-20,ys.max()+20],),
                zaxis = dict(nticks=5, range=[zs.min()-50,0],),),)
    
            fig_network.update_layout(scene_aspectmode='manual',scene_aspectratio=dict(x=4, y=4, z=1))
            #add text
            fig_network['layout']['annotations']+=tuple([dict(text='Well:'+str(Well)+' with Radius:'+str(Radius)+'<br>'+ 
                                              'Top Perf:'+str(float(LeaseSummary_df['TopPerf'][LeaseSummary_df['WELL_NAME']==Well].min()))+
                                              ' | Drill Year:'+str(int(LeaseSummary_df['DRILL_YEAR'][LeaseSummary_df['WELL_NAME']==Well].min()))+
                                              '| Avg TOD in View:'+str(float("{:.1f}".format(AvgTOD)))+'<br>'+ '# of Events:'+
                                              str(#float("{:.1f}".format(
                                              LeaseSummary_df['Event Count'][LeaseSummary_df['WELL_NAME']==Well].mean())+
                                              ' | Avg Event Depth:'+
                                              str(float("{:.1f}".format(
                                                  LeaseSummary_df['Avg Event Depth'][LeaseSummary_df['WELL_NAME']==Well].mean())))+
                                              '<br>'+'# of Intersecting Events:'+
                                              str(float("{:.1f}".format(LeaseSummary_df['Intersection Count'][LeaseSummary_df['WELL_NAME']==Well].mean())))+
                                                '|Depth:'+str(float("{:.1f}".format(LeaseSummary_df['Avg Intersection Depth'][LeaseSummary_df['WELL_NAME']==Well].mean())))+
                                              '<br>'+'# of Intersecting Events After Spud:'+
                                              str(float("{:.1f}".format(LeaseSummary_df['Intersection Count After Spud'][LeaseSummary_df['WELL_NAME']==Well].mean())))+
                                                '|Depth:'+str(float("{:.1f}".format(LeaseSummary_df['Avg Intersection After Spud Depth'][LeaseSummary_df['WELL_NAME']==Well].mean())))+
                                              '<br>'+'Intersecting Events Disorder Value:'+
                                              str(float("{:.1f}".format(LeaseSummary_df['Intersecting Disorder Value'][LeaseSummary_df['WELL_NAME']==Well].mean()))),
                                               align='left',showarrow=False,xref='paper',yref='paper',
                                               x=0.0,y=.93,bordercolor='black',borderwidth=1)])
    
            #set default camera view
            camera = dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=-.3),
                eye=dict(x=-3.5, y=-3.5, z=1)
            )
    
            fig_network.update_layout(scene_camera=camera)
            fig_network.update_layout(hovermode='closest')
    
            #pyo.iplot(fig_network)
            Well=Well.replace(" ","_")
            path=r'//fs01.sentinelpeakresources.local/I Drive/Assets/SJV/Frac_Model_HTML/'+str(Asset)+'/'+str(Well)+'.html'
            pio.write_html(fig_network, file=path, auto_open=False,validate=False)
    
            j=j+1

    assetcount=assetcount+1

# In[208]:


#density_df=Leaseevent_df[['NAD27 Easting','NAD27 Northing','Depth','Field','Lease']]
#Fields=['E AND M']#['KEENE','KELLY','SOUTH CERRITOS','WILLIAMS']<-Lease
#density_df=density_df[density_df['Field'].isin(Fields)]
##density_df=density_df.drop([6],axis=0)
#
#
## In[209]:
#
#
#import matplotlib.pyplot as plt
#
#x_den=density_df['NAD27 Easting']/1000
#y_den=density_df['NAD27 Northing']/1000
#z_den=density_df['Depth']
#x_den=x_den.astype('float')
#y_den=y_den.astype('float')
#z_den=z_den.astype('float')
#
#plt.hist2d(x_den, y_den, bins=(25, 25), cmap=plt.cm.jet)
#
#plt.colorbar()
#plt.show()
#
#
## In[210]:
#
#
#import seaborn as sns
# 
## Basic 2D density plot
#sns.set_style("white")
#sns.kdeplot(x_den, y_den)
#plt.show()
#
#
## In[211]:
#
#
#import matplotlib.pyplot as plt
#import numpy as np
#from scipy.stats import kde
#
## Evaluate a gaussian kde on a regular grid of nbins x nbins over data extents
#nbins=300
#k = kde.gaussian_kde([x_den,y_den])
#xi, yi = np.mgrid[x_den.min():x_den.max():nbins*1j, y_den.min():y_den.max():nbins*1j]
#zi = k(np.vstack([xi.flatten(), yi.flatten()]))
# 
## Make the plot
#plt.pcolormesh(xi, yi, zi.reshape(xi.shape))
#plt.colorbar()
#plt.show()


# In[ ]:


Southflank = ['Keene 20','Keene 33','Keene 69','Keene 70','Keene 71','Keene 72','Keene 73','Keene 74','Keene 76','Keene 77',
'Keene 78','Keene 79','Keene 81','Keene 82','Keene 83','Keene 84','Keene 109','Keene 110','South Cerritos 32','South Cerritos 34',
'South Cerritos 35','South Cerritos 36','Williams 22','Williams 24','Williams 25','Williams 26','Williams 27','Williams 28',
'Williams 3','Keene 7','Williams 11']

