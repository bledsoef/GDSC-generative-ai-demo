import Image from "next/image";
import GeminiAIChatbot from "../../components/GeminiAIChatbot";
export default function Gemini() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-5xl w-full h-full items-center justify-between font-mono text-sm lg:flex">
        <GeminiAIChatbot/>
      </div>
    </main>
  );
}
