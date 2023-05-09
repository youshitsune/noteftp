import streamlit as st
from ftplib import FTP
import os

if not st.session_state:
    st.session_state.clicked = False
tmp = st.empty()

def get_files(server):
    ctx = []
    server.retrlines("NLST", callback=ctx.append)
    return ctx

def get_ctx(ftp, path):
    ctx = []
    ftp.retrbinary(f"RETR {path}", ctx.append)
    for i in range(len(ctx)):
        try:
            ctx[i] = ctx[i].decode("utf-8")
        except Exception:
            st.error("Can't decode this file")
            return ""
            break
            
    return "".join(ctx)

def save(ftp, path, ctx):
    try:
        ftp.delete(path)
    except Exception:
        pass
    with open("file.txt", "wb") as f:
        f.write(ctx.encode("utf-8"))
    ftp.storbinary(f"STOR {path}", open("file.txt", "rb"))
    os.remove("file.txt")

def run(host, user, passwd):
    ftp = FTP(host, user=user, passwd=passwd)
    files = get_files(ftp)
    file = st.sidebar.selectbox("Select a file:", files)
    with tmp.container():
        ctx = st.text_area(f"{file}", value=get_ctx(ftp, file))
        if st.button("Save"):
            save(ftp, file, ctx)


if __name__ == "__main__":
    if not st.session_state.clicked:
        with tmp.form("ftp"):
            host = st.text_input("Host")
            user = st.text_input("Username")
            passwd = st.text_input("Password", type="password")
    
            if st.form_submit_button("Submit"):
                st.session_state.clicked = True
                tmp.empty()
                st.session_state.host = host
                st.session_state.user = user
                st.session_state.passwd = passwd

    if st.session_state.clicked:
        run(st.session_state.host,st.session_state.user,st.session_state.passwd)
