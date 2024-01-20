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
# source_directory= {values['source_directory']}
key_path={key_path}
    """

def generate_docker_command(is_mac, env_path, main_folder_path, json_file_path):
    platform_cmd = "--platform linux/amd64 " if is_mac else ""
    output_volume = os.path.join(main_folder_path, "data/output")
    return f"docker run {platform_cmd}--env-file {env_path} -v {output_volume}:/data/output -v {json_file_path}:/data/gcp_unique.json karthikrathod/data_scraping_docker:latest"

def main():
    st.title("ENV File Generator and Docker Command Creator")

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
    sort_options = ['classic_factor desc', 'citation_count asc', 'year desc']
    subset_options = ['database:astronomy', 'database:physics', 'database:general']

    # Checkboxes for parameters
    st.text("Select Parameters")
    st.caption("Choose the parameters to be included in the dataframe.")
    selected_params = {}
    cols = st.columns(4)  # Adjust the number of columns as needed
    for i, param in enumerate(params_options):
        with cols[i % 4]:  # Adjust the index for the number of columns
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
    
    values['percentile_metric'] = st.text_input("Percentile Metric")
    st.caption("Enter the metric for percentile calculation.")
    
    values['percentile_value'] = st.number_input("Percentile Value", min_value=0.0, max_value=1.0, step=0.01)
    st.caption("Set the percentile value for filtering.")
    
    values['instruction_text'] = st.text_area("Instruction Text")
    st.caption("Provide instructions or descriptions for the data processing.")
    
    values['bucket_name'] = st.text_input("Bucket Name")
    st.caption("Name of the bucket for storing data.")
    
    values['source_directory'] = st.text_input("Source Directory")
    st.caption("Directory path where source files are located.")
    


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

    if st.button("Generate Docker Command"):
        docker_command = generate_docker_command(is_mac, env_file_path, main_folder_path, json_file_path)
        st.text_area("Docker Command", docker_command, height=100)
if __name__ == "__main__":
    main()