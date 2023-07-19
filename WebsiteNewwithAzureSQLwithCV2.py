import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import cv2
import pyodbc
from datetime import datetime

import time

st.set_page_config(page_title="IoT CoE Track 'N' Trace",page_icon=":tada:",layout="wide")

with st.container():
 #st.subheader("Track and Trace Application")
 st.title("IoT CoE Track 'N' Trace")

 with  st.sidebar:
  selected =option_menu(
         menu_title="Stations",
         options=("Material Handling Station","Pinning and Press Station","Drilling Station"),
  )

cnxn_str = ("Driver={ODBC Driver 18 for SQL Server};"
            "Server=tcp:coepocsqlserver.database.windows.net,1433;"
            "Database=coeqrappdb;"
            "UID=coepocadmin;"
            "PWD={Password@123};")
cnxn = pyodbc.connect(cnxn_str)


if selected == "Material Handling Station":
 #st.title("You are on Station3")
 #image = st.camera_input("Show QR code")
 vid = cv2.VideoCapture(0)

 detector = cv2.QRCodeDetector()

 while True:

     # Capture the video frame by frame
     Ret, frame = vid.read()

     data, bbox, straight_qrcode = detector.detectAndDecode(frame)
     if len(data) >0:
         st.write(data)
         temp = str(data)
         x = temp.split()
         st.write(x)
         now = datetime.now()
         cursor = cnxn_str.cursor()
         Insert = "INSERT INTO ioc_coe_poc_blockdatabase.tracking_table (Cube_ID,Station_ID,Current_Status,Date_And_Time) VALUES (%s,%s,%s,%s)"
         val = (x[1], 1, 'Station1 Passed', now)
         cursor.execute(Insert, val)
         cnxn_str.commit()
         sql = "SELECT * FROM ioc_coe_poc_blockdatabase.tracking_table where cube_id=%s"
         adr = (x[1],)
         cursor.execute(sql, adr)
         result = cursor.fetchall()
         df = pd.DataFrame(result,columns=('Tracking_ID', 'Cube_ID', 'Station_ID', 'Current_Status', 'Data_And_Time'))
         hide_table_row_index = """
         <style>
         thead tr th:first-child {display:none}
         tbody th {display:none}
         </style>
         """
         st.markdown(hide_table_row_index, unsafe_allow_html=True)
         st.table(df)
         time.sleep(2)
     # Display the resulting frame
     cv2.imshow('frame', frame)

     #cv2.imshow('frame2',frame)

     # the 'q' button is set as the
     # quitting button you may use any
     # desired button of your choice
     if cv2.waitKey(1) & 0xFF == ord('q'):
         break

 # After the loop release the cap object
 vid.release()
 # Destroy all the windows
 cv2.destroyAllWindows()

if selected == "Pinning and Press Station":
 st.title("You are on Station2")

if selected == "Drilling Station":
 st.title("You are on Station3")

