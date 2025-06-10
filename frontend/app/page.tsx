"use client";

import { useState } from "react";
import FileUpload from "../src/components/FileUpload";
import ScoreDisplay from "../src/components/ScoreDisplay";

interface SectionFeedback {
  summary: string;
  skills: string;
  education: string;
  experience: string;
  grammar: string;
}

export default function Home() {
  const [score, setScore] = useState<number | null>(null);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [sectionFeedback, setSectionFeedback] = useState<SectionFeedback | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async (file: File) => {
    setIsLoading(true);
    setError(null);
    setScore(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8001/analyze", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to analyze resume. Please try again.");
      }

      const data = await response.json();
      setScore(data.score);
      setSuggestions(data.suggestions);
      setSectionFeedback(data.sectionFeedback);
    } catch (err: any) {
      setError(err.message || "An unexpected error occurred.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 sm:p-24">
      <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm text-center mb-12">
        <h1 className="text-4xl font-bold">Resume Analyzer</h1>
        <p className="text-lg mt-2 text-gray-600">
          Upload your resume to get a score and feedback.
        </p>
      </div>

      <div className="w-full max-w-xl">
        <FileUpload onFileUpload={handleFileUpload} isLoading={isLoading} />
      </div>

      {error && (
        <div className="mt-8 text-red-500 bg-red-100 p-4 rounded-lg">
          <p className="font-bold">Error:</p>
          <p>{error}</p>
        </div>
      )}

      <div className="mt-8 w-full max-w-4xl">
        {score !== null && sectionFeedback && suggestions.length > 0 && (
          <ScoreDisplay
            score={score}
            suggestions={suggestions}
            sectionFeedback={sectionFeedback}
          />
        )}
      </div>
    </main>
  );
}
