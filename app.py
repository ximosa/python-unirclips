import streamlit as st
from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
import tempfile

def unir_videos(video_files, nombre_salida):
    try:
        temp_video_files = []
        for video_file in video_files:
            with tempfile.NamedTemporaryFile(suffix=os.path.splitext(video_file.name)[1], delete=False) as tmp_file:
                tmp_file.write(video_file.read())
                temp_video_files.append(tmp_file.name)

        video_clips = [VideoFileClip(file) for file in temp_video_files]
        final_clip = concatenate_videoclips(video_clips, method="compose")
        
        final_clip.write_videofile(
            nombre_salida,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            preset='ultrafast',
            threads=4
        )

        final_clip.close()
        for file in temp_video_files:
            os.remove(file)

        return True, "Videos unidos exitosamente"

    except Exception as e:
        for file in temp_video_files:
            try:
                os.remove(file)
            except:
                pass
        return False, str(e)

def main():
    st.title("Aplicación para Unir Clips de Video")

    video_files = st.file_uploader(
        "Carga los clips de video que quieres unir", 
        type=["mp4", "mov"], 
        accept_multiple_files=True
    )

    nombre_salida = st.text_input(
        "Nombre del video de salida (sin extensión)",
        "video_unido"
    )

    if video_files:
        if st.button("Unir Videos"):
            with st.spinner("Uniendo videos..."):
                nombre_salida_completo = f"{nombre_salida}.mp4"
                success, message = unir_videos(video_files, nombre_salida_completo)
                if success:
                    st.success(message)
                    st.video(nombre_salida_completo)
                    with open(nombre_salida_completo, 'rb') as file:
                         st.download_button(label="Descargar video", data=file, file_name=nombre_salida_completo)
                    st.session_state.video_path = nombre_salida_completo
                else:
                    st.error(message)
    
    if st.session_state.get("video_path"):
        st.markdown(f'<a href="{st.session_state.video_path}" target="_blank">Ver video</a>', unsafe_allow_html=True)


if __name__ == "__main__":
    if "video_path" not in st.session_state:
        st.session_state.video_path = None
    main()
