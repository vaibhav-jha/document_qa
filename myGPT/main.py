from .docs import *
from .mygpt_settings import *
import pickle
import glob
from .mygpt_utils import extract_first_table

class Contract:

    def __init__(self, docs: Optional[Docs] = None):
        self.docs = docs

    def add_docs(self, path='./contracts'):
        # First check and load FAISS index for docs
        try:
            with open("./my_docs.pkl", "rb") as f:
                docs = pickle.load(f)
                print("Loaded from pickle")
        except:
            print("New Docs instance")
            docs = Docs(
                # llm=llm,
                # embeddings=embeddings,
                index_path=INDEX_PATH,
            )

        source_files = glob.glob(f'{path}/*.pdf')
        for f in source_files:
            # this assumes the file names are unique in code
            filename = f.split(f'{path}/')[-1]
            print(f"Processing {filename=}")
            try:
                docs.add(f, citation='File ' + f, key=filename)
            except ValueError:
                print(f'{filename} already existed')
                print(f'{docs._faiss_index}')
                continue

        self.docs = docs

    def ask(self, query, words=200):

        if self.docs is None:
            return "No document to learn from", None

        answer = self.docs.query(query, length_prompt=f"about {words} words")

        ans, table = extract_first_table(answer.formatted_answer)

        return ans, table

    def pickle(self):
        if self.docs is None:
            return "No document(s) to store"
        with open("./my_docs.pkl", "wb") as f:
            pickle.dump(self.docs, f)
