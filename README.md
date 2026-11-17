# Artifacts: cultural context in LLM moderation of children's ads

Anonymous artifact repository for the WWW 2027 short-paper submission. It contains the prompt, the code to collect
and analyse the labels, every model label used in the paper, and the qualitative-review codebook and codes.

## Contents
| Path | What it is |
|---|---|
| `prompt/` | System prompt, answer schema and request format (Appendix A of the paper) |
| `data/labels.csv` | All 35,997 labels: 24 country personas × 500 ads × 3 runs (3 requests failed) |
| `code/prepare_inputs.ipynb` | Builds each ad's input: metadata, Whisper transcript, up to 16 frames |
| `code/run_labels.ipynb` | Sends the requests to the OpenAI API (resumable, parallel) |
| `code/analysis.py` | Reproduces every number in the paper (Table 1, per-country results, RQ3) |
| `code/make_figure.py` | Reproduces Figure 1 |
| `qualitative/` | Codebook, the 11 reviewed ads, all codes, and the template of the coding page used |

## Data
`data/labels.csv` has one row per label:

| Column | Meaning |
|---|---|
| `run` | Run 1, 2 or 3 |
| `batch` | Batch of 12 countries (1 or 2) |
| `country` | The persona's country |
| `muslim_majority` | Whether that country is Muslim-majority |
| `ad` | Ad identifier (see below) |
| `label` | Inappropriate, Child-directed or Irrelevant |
| `concerns` | JSON list of the concerns the model gave (empty unless Inappropriate) |
| `rationale` | The model's rationale |

The ads, their metadata and the country of each impression come from the *safeonline-youtubeads* dataset, which is
available from its authors on request. To respect its data use terms, we do not redistribute ad videos, metadata,
transcripts or impression records. Ads are identified by `sha256(ad_id)[:16]` of the dataset's `ad_id_clean`, so
anyone with access to the dataset can link our labels back to it.

## Reproducing the results
```
pip install pandas numpy scipy matplotlib
python code/analysis.py                                  # RQ1 and RQ2: Table 1, per-country results
python code/analysis.py path/to/videos_dataset.csv       # adds RQ3: where the ads were served
python code/make_figure.py                               # Figure 1
```
The permutation tests use a fixed seed. Collecting new labels needs `code/prepare_inputs.ipynb` (dataset access,
Whisper large-v3) and `code/run_labels.ipynb` (OpenAI API key). Both were run on Kaggle.

## Model and settings
GPT-6 Luna through the OpenAI Responses API, reasoning effort `none`, default sampling settings, up to 16 frames at
low image detail, structured output (`prompt/answer_schema.json`).
