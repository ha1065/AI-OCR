import streamlit as st
import os
import asyncio
from pyzerox import zerox
import json

# Set up environment variables
MODEL = "gemini/gemini-1.5-pro"
os.environ['GEMINI_API_KEY'] = "AIzaSyDl-q1ViANfeKa7VXJzHCEwneHlyiyjXPY"

async def process_pdf(file_path: str):
   
    output_dir = "./output_test"
    result = await zerox(file_path=file_path, model=MODEL, output_dir=output_dir)
    return result

def main():
    st.title("PDF OCR Extractor")
    st.write("Upload a PDF file, and I'll extract the text using an AI-powered OCR model.")

    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

    if uploaded_file is not None:
        # Save uploaded file temporarily
        file_path = f"./{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        st.info("Processing your PDF...")
        
        # Run the OCR function
        result = asyncio.run(process_pdf(file_path))
        
        # Clean up the uploaded file
        os.remove(file_path)

        if hasattr(result, "pages"):
            result_text = "\n\n".join([page.content for page in result.pages])  # Extract text from all pages
        else:
            result_text = str(result)  # Fallback conversion
        # Display result
        st.subheader("Extracted Text:")
        st.text_area("OCR Output", result, height=300)

        
        # Download button
        st.download_button("Download Extracted Text", result_text, file_name="extracted_text.txt")

if __name__ == "__main__":
    main()

# from pyzerox import zerox
# import os
# import json
# import asyncio

# ### Model Setup (Use only Vision Models) Refer: https://docs.litellm.ai/docs/providers ###

# ## placeholder for additional model kwargs which might be required for some models
# kwargs = {}

# ## system prompt to use for the vision model
# custom_system_prompt = None

# # to override
# # custom_system_prompt = "For the below PDF page, do something..something..." ## example

# ###################### Example for OpenAI ######################
# # model = "gpt-4o-mini" ## openai model
# # os.environ["OPENAI_API_KEY"] = "" ## your-api-key


# # ###################### Example for Azure OpenAI ######################
# # model = "azure/gpt-4o-mini" ## "azure/<your_deployment_name>" -> format <provider>/<model>
# # os.environ["AZURE_API_KEY"] = "" # "your-azure-api-key"
# # os.environ["AZURE_API_BASE"] = "" # "https://example-endpoint.openai.azure.com"
# # os.environ["AZURE_API_VERSION"] = "" # "2023-05-15"


# ###################### Example for Gemini ######################
# model = "gemini/gemini-1.5-pro" ## "gemini/<gemini_model>" -> format <provider>/<model>
# os.environ['GEMINI_API_KEY'] = "AIzaSyDl-q1ViANfeKa7VXJzHCEwneHlyiyjXPY" # your-gemini-api-ke


# ###################### Example for Anthropic ######################
# # model="claude-3-opus-20240229"
# # os.environ["ANTHROPIC_API_KEY"] = "" # your-anthropic-api-key

# # ###################### Vertex ai ######################
# # model = "vertex_ai/gemini-1.5-flash-001" ## "vertex_ai/<model_name>" -> format <provider>/<model>
# # ## GET CREDENTIALS
# # ## RUN ##
# # # !gcloud auth application-default login - run this to add vertex credentials to your env
# # ## OR ##
# # file_path = 'path/to/vertex_ai_service_account.json'

# # # Load the JSON file
# # with open(file_path, 'r') as file:
# #     vertex_credentials = json.load(file)

# # # Convert to JSON string
# # vertex_credentials_json = json.dumps(vertex_credentials)

# # vertex_credentials=vertex_credentials_json

# # ## extra args
# # kwargs = {"vertex_credentials": vertex_credentials}

# ###################### For other providers refer:  ######################

# # Define main async entrypoint
# async def main():
#     file_path = r"C:\Users\HaiderAhmed\Downloads\NCAA_0007B_0014.pdf" ## local filepath and file URL supported

#     ## process only some pages or all
#     select_pages = None ## None for all, but could be int or list(int) page numbers (1 indexed)

#     output_dir = "./output_test" ## directory to save the consolidated markdown file
#     result = await zerox(file_path=file_path, model=model, output_dir=output_dir,
#                         custom_system_prompt=custom_system_prompt,select_pages=select_pages, **kwargs)
#     return result


# # run the main function:
# result = asyncio.run(main())

# # print markdown result
# print(result)