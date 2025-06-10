'use client';

import { useState } from 'react';
import FileUpload from '../components/FileUpload';
import ScoreDisplay from '../components/ScoreDisplay';

interface AnalysisResult {
  score: number;
  suggestions: string[];
  sectionFeedback: {
    summary: string;
    skills: string;
    education: string;
    experience: string;
    grammar: string;
  };
}

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async (file: File) => {
    setIsLoading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/analyze-resume', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to analyze resume');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError('Failed to analyze resume. Please try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Resume Analyzer</h1>
          <p className="mt-2 text-gray-600">
            Upload your resume to get detailed feedback and suggestions for improvement
          </p>
        </div>

        <div className="space-y-8">
          <FileUpload onFileUpload={handleFileUpload} isLoading={isLoading} />

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative">
              {error}
            </div>
          )}

          {result && !error && (
            <ScoreDisplay
              score={result.score}
              suggestions={result.suggestions}
              sectionFeedback={result.sectionFeedback}
            />
          )}
        </div>
      </div>
    </main>
  );
} 