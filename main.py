import streamlit as st
from ftplib import FTP

if not st.session_state:
    st.session_state.clicked = False
tmp = st.empty()

def get_files(server):
    ctx = ["None"]
    server.retrlines("NLST", callback=ctx.append)
    return ctx

def run(host, user, passwd):
    ftp = FTP(host, user=user, passwd=passwd)
    files = get_files(ftp)
    file = st.sidebar.selectbox("Select a file:", files)
    with tmp.container():
        if file == "None":
            st.write("# Select a file")
        else:
            st.write("# You successfully selected a file")


if __name__ == "__main__":
    if not st.session_state.clicked:
        with tmp.form("ftp"):
            host = st.text_input("Host")
            user = st.text_input("Username")
            passwd = st.text_input("Password")
    
            if st.form_submit_button("Submit"):
                st.session_state.clicked = True
                tmp.empty()
                st.session_state.host = host
                st.session_state.user = user
                st.session_state.passwd = passwd

    if st.session_state.clicked:
        run(st.session_state.host,st.session_state.user,st.session_state.passwd)
