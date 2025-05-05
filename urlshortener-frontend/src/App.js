import React, { useState } from 'react';
import { CopyToClipboard } from 'react-copy-to-clipboard';

function App() {
  const [originalUrl, setOriginalUrl] = useState('');
  const [shortUrl, setShortUrl] = useState('');
  const [copied, setCopied] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch('http://localhost:8000/shorten/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ original_url: originalUrl }),
    });
    const data = await res.json();
    setShortUrl(`http://localhost:8000/${data.short_code}/`);
    setCopied(false); // Reset copied state when new URL is generated
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          value={originalUrl}
          onChange={e => setOriginalUrl(e.target.value)}
          placeholder="Enter URL"
        />
        <button type="submit">Shorten</button>
      </form>
      {shortUrl && (
        <>
          <p>
            Short URL: <a href={shortUrl} target="_blank" rel="noopener noreferrer">{shortUrl}</a>
          </p>
          <CopyToClipboard text={shortUrl} onCopy={() => setCopied(true)}>
            <button>{copied ? 'Copied' : 'Copy'}</button>
          </CopyToClipboard>
        </>
      )}
    </div>
  );
}

export default App;