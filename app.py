import streamlit as st
import io
import os

def generate_env_content(values, selected_params):
    params_str = ','.join(param for param, selected in selected_params.items() if selected)
    key_path = "data/gcp_unique.json"  # Fixed value for key_path
    return f"""
API_TOKEN={values['api_token']}
QUERY={values['query']}
MAX_ROWS={values['max_rows']}
START={values['start']}
PARAMS={params_str}
SORT={values['sort']}
SUBSET={values['subset']}
PERCENTILE_FILTERING={values['percentile_filtering']}
PERCENTILE_METRIC={values['percentile_metric']}
PERCENTILE_VALUE={values['percentile_value']}
INSTRUCTION_TEXT={values['instruction_text']}
bucket_name={values['bucket_name']}
upload_to_gcp={values['upload_to_gcp']}
key_path={key_path}
    """

def generate_docker_command(is_mac, env_path, main_folder_path, json_file_path, container_name="data_extraction_container"):
    platform_cmd = "--platform linux/amd64 " if is_mac else ""
    output_volume = os.path.join(main_folder_path, "data/output")
    # Including the container name in the command with `--name` flag
    return f"docker run --name {container_name} {platform_cmd}--env-file {env_path} -v {output_volume}:/data/output -v {json_file_path}:/data/gcp_unique.json karthikrathod/data_scraping_docker:latest"

def main():
    background_image = """
    <style>
    [data-testid="stAppViewContainer"] > .main {
        background-image: url("https://images.unsplash.com/photo-1524334228333-0f6db392f8a1?q=80&w=2970&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
        background-position: center;  
        background-repeat: no-repeat;
    }
    </style>
    """

    st.markdown(background_image, unsafe_allow_html=True)
    st.title("Environmental setup Generator and Docker Command Creator")

    # Define parameters and options
    params_options =  [
    "abstract",
    "alternate_bibcode",
    "alternate_title",
    "author",
    "bibcode",
    "bibgroup",
    "bibstem",
    "body",
    "citation_count",
    "doi",
    "id",
    "keyword",
    "read_count",
    "title",
    "year"
]
    sort_options = ['classic_factor desc', 'classic_factor asc',
    'citation_count desc',
    'citation_count asc',
    'read_count desc',
    'read_count asc'
]
    subset_options = ['database:astronomy', 'database:physics', 'database:general',"database:earthsicence"]
    metric_options = ['read_count', 'citation_count', 'classic_factor']


  # Checkboxes for parameters with bibcode made compulsory
    st.text("Select Parameters")
    st.caption("Choose the parameters to be included in the dataframe. 'bibcode' is selected by default and is required.")
    selected_params = {"bibcode": True}  # Pre-selecting bibcode as true
    cols = st.columns(4)  # Adjust the number of columns as needed
    for i, param in enumerate(params_options):
        if param == "bibcode":
            st.checkbox("bibcode", value=True, disabled=True, key="bibcode")  # Making bibcode checkbox always selected and disabled
        else:
            with cols[i % 4 - 1]:  # Adjusting index for columns considering bibcode is always selected
                selected_params[param] = st.checkbox(param, key=param)

    # Create input fields with explanations
    values = {}
    values['api_token'] = st.text_input("API Token")
    st.caption("Enter the NASA/ADS API token for authentication.[Create ADS API Token](https://ui.adsabs.harvard.edu/user/settings/token)")
    
    values['query'] = st.text_input("Query")
    st.caption("Define the query to filter the data. eg: year:2019-2020. [More ideas](https://ui.adsabs.harvard.edu/) for queries.")
    
    values['max_rows'] = st.number_input("Max Rows", min_value=0)
    st.caption("Set the maximum number of rows to retrieve.")
    
    values['start'] = st.number_input("Start", min_value=0)
    st.caption("Specify the starting point for data retrieval.")
    
    values['sort'] = st.selectbox("Sort", sort_options)
    st.caption("Choose how to sort the data.")
    
    values['subset'] = st.selectbox("Subset", subset_options)
    st.caption("Select the subset of data to work with.")
    
    values['percentile_filtering'] = st.selectbox("Percentile Filtering", ["True", "False"])
    st.caption("Enable or disable percentile filtering.")
    
    values['percentile_metric']  = st.selectbox("percentile_metric", metric_options)
    st.caption("Enter the metric for percentile calculation.")
    
    values['percentile_value'] = st.number_input("Percentile Value", min_value=0.0, max_value=1.0, step=0.01)
    st.caption("Set the percentile value for filtering.")
    
    values['instruction_text'] = st.text_area("Instruction Text")
    st.caption("Provide instructions or descriptions for the data processing.")
    
    values['bucket_name'] = st.text_input("Bucket Name")
    st.caption("Name of the bucket for storing data.")
    
    values['upload_to_gcp'] = st.selectbox("Upload to GCP", ["True", "False"])
    st.caption("Enable or disable uploading to GCP.")
    


    if st.button("Generate .ENV File"):
        env_content = generate_env_content(values, selected_params)
        st.text_area("ENV File Content", env_content, height=400)
        # To handle the file download
        # towrite = io.BytesIO()
        # towrite.write(env_content.encode('utf-8'))
        # towrite.seek(0)
        # st.download_button(label="Download .ENV File",
        #                    data=towrite,
        #                    file_name="new.env",
        #                    mime="text/plain")

    # Docker Command Creator Section
    st.header("Docker Command Creator")
    is_mac = st.checkbox("Is the host machine a Mac?")
    env_file_path = st.text_input("Path to .env file")
    main_folder_path = st.text_input("Path to main folder")
    json_file_path = st.text_input("Path to GCP credentials JSON file")
    container_name = st.text_input("Container Name", value="data_extraction_container")  # Default value provided

    if st.button("Generate Docker Command"):
        docker_command = generate_docker_command(is_mac, env_file_path, main_folder_path, json_file_path, container_name)
        st.text_area("Docker Command", docker_command, height=100)
if __name__ == "__main__":
    main()