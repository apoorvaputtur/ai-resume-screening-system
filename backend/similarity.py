import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from resume_parser import extract_text_from_pdf, extract_text_from_docx
from text_preprocessing import clean_text


def rank_resumes(job_description, resume_folder):
    resumes = []
    names = []

    for file in os.listdir(resume_folder):
        path = os.path.join(resume_folder, file)

        # -------- SELECT PARSER BASED ON FILE --------
        if file.lower().endswith(".pdf"):
            text = extract_text_from_pdf(path)

        elif file.lower().endswith(".docx"):
            text = extract_text_from_docx(path)

        else:
            continue  # skip unsupported files

        resumes.append(clean_text(text))
        names.append(file)

    if not resumes:
        return []

    documents = [clean_text(job_description)] + resumes

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(documents)

    similarity_scores = cosine_similarity(vectors[0:1], vectors[1:])[0]

    results = []
    for i, score in enumerate(similarity_scores):
        results.append({
            "name": names[i],
            "score": round(score * 100, 2),
            "resume_url": f"/download/{names[i]}"
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results
