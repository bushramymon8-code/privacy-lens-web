import streamlit as st
from PIL import Image
import piexif
import io
import pandas as pd

st.set_page_config(page_title="Privacy Lens Pro", page_icon="🛡️")

st.title("🛡️ Privacy Lens Pro")
st.write("Apni images upload karein aur unka hidden metadata (EXIF) scan ya remove karein.")

# File Uploader
uploaded_files = st.file_uploader("Images select karein (JPG, JPEG, PNG)", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

if uploaded_files:
    st.subheader(f"Total Files: {len(uploaded_files)}")
    
    # Buttons for Actions
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Scan Metadata"):
            for uploaded_file in uploaded_files:
                st.markdown(f"---")
                st.write(f"**FILE:** {uploaded_file.name}")
                try:
                    img = Image.open(uploaded_file)
                    exif_data = img.info.get("exif")

                    if exif_data:
                        data = piexif.load(exif_data)
                        risk = "LOW Risk"
                        
                        # Show metadata in a table or expander
                        with st.expander("Raw Metadata Dekhein"):
                            for ifd in data:
                                if data[ifd]:
                                    st.write(f"**Section: {ifd}**")
                                    for tag in data[ifd]:
                                        st.text(f"Tag {tag}: {data[ifd][tag]}")
                                        if "GPS" in str(ifd):
                                            risk = "🔴 HIGH Risk (Location Data Found)"
                        
                        st.info(f"**RISK LEVEL:** {risk}")
                    else:
                        st.success("RISK LEVEL: Clean (No metadata found)")
                except Exception as e:
                    st.error(f"Error scanning {uploaded_file.name}: {e}")

    with col2:
        if st.button("✨ Remove & Download"):
            for uploaded_file in uploaded_files:
                try:
                    img = Image.open(uploaded_file)
                    # Metadata remove karne ka sab se asan tareeqa
                    data = list(img.getdata())
                    clean_img = Image.new(img.mode, img.size)
                    clean_img.putdata(data)
                    
                    # Buffer mein save karna taake download ho sakay
                    buf = io.BytesIO()
                    clean_img.save(buf, format="JPEG")
                    byte_im = buf.getvalue()
                    
                    st.download_button(
                        label=f"Download Clean {uploaded_file.name}",
                        data=byte_im,
                        file_name=f"clean_{uploaded_file.name}",
                        mime="image/jpeg"
                    )
                except Exception as e:
                    st.error(f"Error cleaning {uploaded_file.name}")

    # CSV Report Logic
    if st.button("📊 Generate CSV Report"):
        report_data = []
        for f in uploaded_files:
            report_data.append({"File Name": f.name, "Status": "Checked & Processed"})
        
        df = pd.DataFrame(report_data)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV Report", csv, "privacy_report.csv", "text/csv")
